import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import type { JSX } from "react";


export function PrivateRoute({ children }: { children: JSX.Element }) {
  const { estado } = useAuth();

  if (!estado.token) {
    return <Navigate to="/login" />;
  }

  return children;
}
