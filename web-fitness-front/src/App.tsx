import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { PrivateRoute } from "./routes/PrivateRoute";
import Inicio from "./pages/Inicio";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Registro from "./pages/Registro";
import Ejercicios from "./pages/Ejercicios";
import NuevoEjercicio from "./pages/NuevoEjercicio";



function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Inicio />} />
          <Route path="/login" element={<Login />} />
          <Route path="/registro" element={<Registro />} />
          <Route path="/ejercicios" element={<PrivateRoute><Ejercicios /></PrivateRoute>} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/ejercicios/nuevo" element={<PrivateRoute><NuevoEjercicio /></PrivateRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
