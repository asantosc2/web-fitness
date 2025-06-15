import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { PrivateRoute } from "./routes/PrivateRoute";
import Inicio from "./pages/Inicio";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Registro from "./pages/Registro";
import Ejercicios from "./pages/Ejercicios";
import NuevoEjercicio from "./pages/NuevoEjercicio";
import Rutinas from "./pages/Rutinas";
import RutinaDetalle from "./pages/RutinaDetalle";
import RutinaNueva from "./pages/RutinaNueva";
import EditarRutina from "./pages/EditarRutina";
import SesionDetalle from "./pages/SesionDetalle";



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
          <Route path="/rutinas" element={<PrivateRoute><Rutinas /></PrivateRoute>} />
          <Route path="/rutinas/:id" element={<RutinaDetalle />} />
          <Route path="/rutinas/nueva" element={<PrivateRoute><RutinaNueva /></PrivateRoute>} />
          <Route path="/rutinas/:id/editar" element={<PrivateRoute><EditarRutina /></PrivateRoute>} />
          <Route path="/sesiones/:id" element={<SesionDetalle />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
