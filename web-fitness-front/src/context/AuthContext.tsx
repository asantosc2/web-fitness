import { createContext, useContext, useReducer } from "react";

type Estado = {
  token: string | null;
  usuario: any | null;
};

type Accion =
  | { type: "LOGIN"; payload: { token: string; usuario: any } }
  | { type: "LOGOUT" };

const estadoInicial: Estado = {
  token: localStorage.getItem("token"),
  usuario: localStorage.getItem("usuario")
    ? JSON.parse(localStorage.getItem("usuario")!)
    : null,
};

function authReducer(state: Estado, action: Accion): Estado {
  switch (action.type) {
    case "LOGIN":
      localStorage.setItem("token", action.payload.token);
      localStorage.setItem("usuario", JSON.stringify(action.payload.usuario));
      return { token: action.payload.token, usuario: action.payload.usuario };
    case "LOGOUT":
      localStorage.removeItem("token");
      localStorage.removeItem("usuario");
      return { token: null, usuario: null };
    default:
      return state;
  }
}

const AuthContext = createContext<{
  estado: Estado;
  login: (token: string, usuario: any) => void;
  logout: () => void;
}>({
  estado: estadoInicial,
  login: () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [estado, dispatch] = useReducer(authReducer, estadoInicial);

  const login = (token: string, usuario: any) => {
    dispatch({ type: "LOGIN", payload: { token, usuario } });
  };

  const logout = () => {
    dispatch({ type: "LOGOUT" });
  };

  return (
    <AuthContext.Provider value={{ estado, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
