import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import logo from "../assets/logo.png";
import { useState } from "react";

export default function Navbar() {
  const { estado } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  return (
    <nav className="bg-white shadow-md fixed top-0 w-full z-50">
      <div className="w-full h-16 flex items-center justify-between px-4 md:px-8">
        {/* Logo + Nombre */}
        <div className="flex items-center gap-3">
          <img src={logo} alt="Liftio Logo" className="h-12 w-auto object-contain" />
          <span className="text-xl font-bold text-blue-600">Liftio</span>
        </div>

        {/* Hamburguesa en móvil */}
        <div className="md:hidden">
          <button onClick={() => setOpen(!open)} className="text-gray-800 text-2xl">
            ☰
          </button>
        </div>

        {/* Menú en escritorio */}
        <div className="hidden md:flex items-center gap-6 text-sm font-semibold">
          {estado.token ? (
            <>
              <Link to="/dashboard" className="hover:text-blue-600 transition">Dashboard</Link>
              <button
                onClick={() => {
                  localStorage.clear();
                  navigate("/");
                  window.location.reload();
                }}
                className="text-red-600 hover:text-red-800 transition"
              >
                Cerrar sesión
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-blue-600 transition">Iniciar sesión</Link>
              <Link to="/registro" className="hover:text-blue-600 transition">Registrarse</Link>
            </>
          )}
        </div>
      </div>

      {/* Menú desplegable en móvil */}
      {open && (
        <div className="md:hidden bg-white shadow-inner flex flex-col items-start gap-4 px-6 py-4 text-sm font-semibold">
          {estado.token ? (
            <>
              <Link to="/dashboard" onClick={() => setOpen(false)} className="hover:text-blue-600 transition">Dashboard</Link>
              <button
                onClick={() => {
                  localStorage.clear();
                  navigate("/");
                  window.location.reload();
                }}
                className="text-red-600 hover:text-red-800 transition"
              >
                Cerrar sesión
              </button>
            </>
          ) : (
            <>
              <Link to="/login" onClick={() => setOpen(false)} className="hover:text-blue-600 transition">Iniciar sesión</Link>
              <Link to="/registro" onClick={() => setOpen(false)} className="hover:text-blue-600 transition">Registrarse</Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
}
