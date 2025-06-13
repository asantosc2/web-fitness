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
    const res = await fetch("http://localhost:8000/login", {
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
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: `url(${fondoLanding})` }}
    >
      <Navbar />
      <div className="bg-black bg-opacity-60 absolute inset-0"></div>
      <form
        onSubmit={handleSubmit}
        className="relative bg-white bg-opacity-90 shadow-lg rounded-lg p-8 max-w-md w-full"
      >
        <h2 className="text-3xl font-bold text-center text-blue-600 mb-6">
          Iniciar Sesión en Liftio
        </h2>

        {error && <p className="text-red-500 text-center mb-4">{error}</p>}

        <input
          className="border p-3 rounded-md w-full mb-4"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          className="border p-3 rounded-md w-full mb-4"
          placeholder="Contraseña"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-3 rounded-md w-full font-semibold hover:bg-blue-700 transition"
        >
          Entrar
        </button>
      </form>
    </div>
  );
}
