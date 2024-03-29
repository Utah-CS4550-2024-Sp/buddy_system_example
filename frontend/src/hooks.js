import { useContext } from "react";
import { AuthContext } from "./context/auth";
import { UserContext } from "./context/user";
import api from "./utils/api";

const useApi = () => {
  const { token } = useAuth();
  return api(token);
}

const useApiWithoutToken = () => {
  return api();
}

const useAuth = () => useContext(AuthContext);

const useUser = () => useContext(UserContext);

export {
  useApi,
  useApiWithoutToken,
  useAuth,
  useUser,
};

