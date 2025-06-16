import { useState } from "react";
import { useNavigate } from "react-router-dom";
import fondoLanding from "../assets/fondo-landing.jpg";
import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch(`${import.meta.env.VITE_API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (res.ok) {
      const data = await res.json();
      login(data.access_token, data.usuario);
      navigate("/dashboard");
    } else {
      setError("Credenciales inválidas");
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center relative"
      style={{ backgroundImage: `url(${fondoLanding})` }}
    >
      <Navbar />
      <div className="absolute inset-0 bg-gradient-to-br from-black via-gray-900 to-blue-900 opacity-70"></div>

      <form
        onSubmit={handleSubmit}
        className="relative bg-white bg-opacity-95 shadow-2xl rounded-xl p-10 w-full max-w-md"
      >
        <h2 className="text-3xl font-extrabold text-center text-blue-700 mb-6">
          Iniciar Sesión en Liftio
        </h2>

        {error && (
          <p className="text-red-600 text-center font-medium mb-4">{error}</p>
        )}

        <input
          className="border border-gray-300 p-3 rounded-lg w-full mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          className="border border-gray-300 p-3 rounded-lg w-full mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Contraseña"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg w-full font-semibold transition"
        >
          Entrar
        </button>

        <div className="mt-6 text-center text-sm text-gray-700">
          ¿No tienes cuenta?{" "}
          <button
            type="button"
            onClick={() => navigate("/registro")}
            className="text-blue-600 hover:underline font-semibold"
          >
            Regístrate aquí
          </button>
        </div>
      </form>
    </div>
  );
}
