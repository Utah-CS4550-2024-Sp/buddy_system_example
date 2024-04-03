# buddy system

## deployment

### backend

the basic steps for deployment are:
1. package our backend code and dependencies
2. deploy our packaged code
3. get the database connected

#### build backend package

we will use `pip` to install our dependencies. if we are using `poetry` as our package
manager, we will need to export our dependencies for `pip` to consume.

before doing this, we need to add in whatever additional dependencies are required for our
deploy. for deployments to lambda, we need `mangum`. and for a PostgreSQL database in RDS,
we need `psycopg2-binary`. if your deploy will be using SQLite, don't worry about adding
`psycopg2`.

```bash
poetry add mangum
poetry add psycopg2-binary
```

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

in the command above, the `-f` argument is the format for the export and the `--output` is
the actual file where we will write the dependencies. you can pick a different filename if
you prefer.

now that we have our dependencies in a format that `pip` understands, we can install our
dependencies to a target folder, for example `build`. here is the basic command to do
that.

```bash
python -m pip install -r requirements.txt -t build
```

however, depending on the architecture of your machine, you may need to specify a
different architecture for the dependencies. in my case, using macOS with `amd`
architecture, i need to specify `x86_64` architecture in order to deploy to AWS Lambda, so
i used the following command.

```bash
python -m pip install \
-r requirements.txt \
-t build \
--platform manylinux2014_x86_64 \
--only-binary=:all:
```

now that we have our dependencies in the `build` folder, we want to zip that folder up.

```bash
cd build
zip -r9 ../build.zip ./
cd ..
```

the last step is to add our backend to the build.

```bash
zip -ur build.zip ./backend
```

**note**: if you want to minimize the size of your deploy, you can safely delete all of
the `__pycache__` folders efore adding the backend to the build.

#### deploy packaged code

we will focus on deploying to AWS Lambda in two scenarios: where the lambda function is
connected to EFS (elastic file system) and the database lives there; and where the we host
the data in a managed database in RDS (relation database service). the first scenario
works, but is not a good solution for a production deployment. the second scenario is a
better long term solution.

in order to work with AWS Lambda and AWS ApiGateway, we need a new dependency that will
translate lambda events/context into what FastAPI is expecting and to translate FastAPI
responses into what ApiGateway is expecting. this dependency is called `mangum`, which we
added above. we need to add two lines to our `backend/main.py`. first the import at the top.

```python
from mangum import Mangum
```

then a lambda handler at the bottom.
```python
lambda_handler = Mangum(app)
```

in either case, we need to put the lambda function in a VPC (virtual private cloud).
navigate to the VPC console in the AWS console. decide which VPC to use (for example, the
default VPC that comes with your account) and find the `Subnet ID` for the subnets
associated to the VPC that will be used later, eg, `subnet-{{hex1}}` and `subnet-{{hex2}}`.
next navigate to the Security Groups in the EC2 console. choose a security group to use
(for example, the default one) and make note of the `Security group ID`, eg `sg-{{hex3}}`.

we will also need to create an execution role for our lambda function. navigate to the
Roles page in the IAM console and create a role. it will be a `AWS service` role and the
`Use case` will be Lambda. we need to attach some policies to give permissions to the
lambda. search for the `AWSLambdaBasicExecutionRole`, `AWSLambdaVPCAccessExecutionRole`,
and `AWSXRayDaemonWriteAccess` policies and select them, then click `Next`. choose a
meaningful role name, for example `buddy-system-lambda-execution-role`, and then click
`Create role`. we will need to add another policy to the role later on, depending on what
the scenario.

##### EFS

navigate to the EFS console and create a file system. make sure to create it in the VPC
that you decided to use above. once you have a file system, you need to create an access
point for that file system. it's good practice to name it so that you know what it is used
for, for example `buddy-system-lambda` or something. for the root directory path, choose
`/mnt/efs`. for the POSIX user, use 1000 for `User ID` and `Group ID`. for the root
directory creation permissions, use 1000 for `Owner user ID` and `Owner group ID` and use
0777 for `Access point permissions`. once you create the access point, make note of the
Access point ARN, of the form
`arn:aws:elasticfilesystem:{{region}}:{{account}}:access-point/{{access-point-id}}`.

we need to update our database code to use the local database for development and the EFS
database for deployment. we can use an environment variable `DB_LOCATION` to decide which
to use. we also don't need to print all of the database transactions for our deployment,
so we'll define `echo` differently as well. you can update your `database.py` file to have
some code similar to the following.

```python
if os.environ.get("DB_LOCATION") == "EFS":
    db_url = "sqlite:////mnt/efs/buddy_system.db"
    echo = False
else:
    db_url = "sqlite:///backend/buddy_system.db"
    echo = True

engine = create_engine(db_url, echo=echo, connect_args={"check_same_thread": False})
```

once we make the update, we need to update our zip file again.

```bash
zip -ur build.zip ./backend
```

we can now create a lambda function via the Lambda console or via the command line.

1. console
    a. click to create a function. choose a good name, for example `buddy-system`.
    b. choose `Python 3.11` as the runtime.
    c. choose `x86_64` as the architecture.
    d. choose `buddy-system-lambda-execution-role` for the execution role.
    e. under advanced settings, click on `Enable VPC`, select the VPC chosen above, select
    the subnets from above, and select the security group from above.
    f. click `Create function`.
    g. under `Code`, click on `Upload from` and choose the zip file `build.zip`.
    h. under `Code`, edit the runtime settings, and update the handler to
    `backend.main.lambda_handler`.
    i. under `Configuration > General configuration`, edit the timeout to be 10 seconds
    and the memory to be 1024 MB.
    j. under `Configuration > Environment variables`, add an environment variable with key
    `DB_LOCATION` and value `EFS`.
    k. under `Configuration > File systems`, add the file system/access point you created
    above with `/mnt/efs` as the local mount path.

2. command line
    ```bash
    aws lambda create-function \
    --function-name buddy-system \
    --runtime python3.11 \
    --role {{ARN for buddy-system-lambda-execution-role}} \
    --handler backend.main.lambda_handler \
    --zip-file fileb://build.zip \
    --memory-size 1024 \
    --timeout 10
    --environment "Variables={DB_LOCATION=EFS}" \
    --vpc-config SubnetIds=subnet-{{hex1}},subnet-{{hex2}},SecurityGroupIds=sg-{{hex3}} \
    --file-system-configs Arn={{ARN for buddy-system-lambda access point}},LocalMountPath=/mnt/efs
    ```

##### RDS

navigate to the RDS console and create a database. i used `Easy create` with `PostgreSQL`
and the `Free tier` DB instance size. choose a suitable name for your database, eg
`buddy-system`. choose a username, eg `postgres`. click on `Self managed` for password,
choose a secure password and store it somewhere (like a password manager, for example).
you can use a different relational database if you prefer, but the rest of the docs will
assume a postgresql database. make note of the database Endpoint and Port.

we need to update our database code to use the local database for development and the RDS
database for deployment. we can use an environment variable `DB_LOCATION` to decide which
to use. we also don't need to print all of the database transactions for our deployment,
so we'll define `echo` differently as well. finally, the `check_same_thread` connect
argument is not part of postgres, so it needs to be discarded. you can update your
`database.py` file to have some code similar to the following.

```python
if os.environ.get("DB_LOCATION") == "RDS":
    username = os.environ.get("PG_USERNAME")
    password = os.environ.get("PG_PASSWORD")
    endpoint = os.environ.get("PG_ENDPOINT")
    port = os.environ.get("PG_PORT")
    db_url = f"postgresql://{username}:{password}@{endpoint}:{port}/{username}"
    echo = False
    connect_args = {}
else:
    db_url = "sqlite:///backend/buddy_system.db"
    echo = True
    connect_args = {"check_same_thread": False}

engine = create_engine(db_url, echo=echo, connect_args=connect_args)
```

once we make the update, we need to update our zip file again.

```bash
zip -ur build.zip ./backend
```

we can now create a lambda function via the Lambda console or via the command line.

1. console
    a. click to create a function. choose a good name, for example `buddy-system`.
    b. choose `Python 3.11` as the runtime.
    c. choose `x86_64` as the architecture.
    d. choose `buddy-system-lambda-execution-role` for the execution role.
    e. under advanced settings, click on `Enable VPC`, select the VPC chosen above, select
    the subnets from above, and select the security group from above.
    f. click `Create function`.
    g. under `Code`, click on `Upload from` and choose the zip file `build.zip`.
    h. under `Code`, edit the runtime settings, and update the handler to
    `backend.main.lambda_handler`.
    i. under `Configuration > General configuration`, edit the timeout to be 10 seconds
    and the memory to be 1024 MB.
    j. under `Configuration > Environment variables`, add environment variables with the
    following keys and values.
        i. key: `DB_LOCATION`, value: `RDS`
        ii. key: `PG_USERNAME`, value: `postgres` (or whatever you chose)
        iii. key: `PG_PASSWORD`, value: the password you chose
        iv: key: `PG_ENDPOINT`, value: the endpoint for your database
        v: key: `PG_PORT`, value: the port for your database

2. command line
    ```bash
    aws lambda create-function \
    --function-name buddy-system \
    --runtime python3.11 \
    --role {{ARN for buddy-system-lambda-execution-role}} \
    --handler backend.main.lambda_handler \
    --zip-file fileb://build.zip \
    --memory-size 1024 \
    --timeout 10
    --environment "Variables={DB_LOCATION=RDS,PG_USERNAME=postgres,PG_PASSWORD=yourpasswordhere,PG_ENDPOINT=yourendpointhere,PG_PORT=yourporthere}" \
    --vpc-config SubnetIds=subnet-{{hex1}},subnet-{{hex2}},SecurityGroupIds=sg-{{hex3}} \
    ```

#### seed the new database

in our situation, it will be useful to seed the database with our initial data, especially
since the API is not fully functional.

one solution to this is to create a lambda that can be run one time to seed the database.
in this codebase, there is a file at `backend/seed_database.py` with code to add
everything from the `fake_db.json` to the database. we need to create a handler for a
lambda that calls that code. in order to do that, the original code was wrapped in a
function called `seed_database` and a return value was defined with the counts of users
and animals added to the database. then we add the handler for the lambda function as
follows:

```python
def lambda_handler(event, context):
    try:
        result = seed_database()
        return {
            "statusCode": 200,
            "body": json.dumps(result),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
```

the zip file needs to be updated once again.

```bash
zip -ur build.zip ./backend
```

we create a new lambda function for seeding the database. it will be the same as the other
one (whichever scenario you chose), except that the `function-name` should be something
like `buddy-system-db-seeder`, the `handler` should be
`backend.seed_database.lambda_handler`, and the `timeout` should be 60 seconds just in
case it takes a little bit to add everything to the database.

from the Lambda console, you can `Test` the new function to have it run once. it should
show you how much data was added to the database according to the return value of the
`seed_database` function. alternatively, you can invoke the function from the command
line, use `aws lambda invoke help` for the options.


