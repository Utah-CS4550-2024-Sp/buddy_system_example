import { setupServer } from "msw/node";
import { handlers } from "./handlers";

console.log(handlers);

const server = setupServer(...handlers);

export { server };
