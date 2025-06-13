import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import fondoLanding from "../assets/fondo-landing.jpg";
import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";

export default function Registro() {
    const navigate = useNavigate();
    const { estado } = useAuth();

    useEffect(() => {
        if (estado.token) {
            navigate("/dashboard");
        }
    }, [estado.token]);
    const [formData, setFormData] = useState({
        nombre: "",
        apellido: "",
        email: "",
        fecha_nacimiento: "",
        password: "",
        confirm: "",
    });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        if (formData.password !== formData.confirm) {
            return setError("Las contraseñas no coinciden");
        }

        try {
            setLoading(true);
            const res = await fetch("http://localhost:8000/usuarios", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    nombre: formData.nombre,
                    apellido: formData.apellido,
                    email: formData.email,
                    fecha_nacimiento: formData.fecha_nacimiento,
                    password: formData.password,
                }),
            });

            if (!res.ok) throw new Error("Error en el registro");
            navigate("/login");
        } catch (err) {
            setError("No se pudo registrar. Verifica los datos.");
        } finally {
            setLoading(false);
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
                className="relative bg-white bg-opacity-90 shadow-lg rounded-lg p-8 max-w-lg w-full"
            >
                <h2 className="text-3xl font-bold text-center text-blue-600 mb-6">
                    Crear cuenta en Liftio
                </h2>

                {error && <p className="text-red-500 text-center mb-4">{error}</p>}

                <input
                    type="text"
                    name="nombre"
                    placeholder="Nombre"
                    value={formData.nombre}
                    onChange={handleChange}
                    required
                    className="w-full mb-4 p-3 border rounded-md"
                />
                <input
                    type="text"
                    name="apellido"
                    placeholder="Apellido"
                    value={formData.apellido}
                    onChange={handleChange}
                    required
                    className="w-full mb-4 p-3 border rounded-md"
                />
                <input
                    type="email"
                    name="email"
                    placeholder="Correo electrónico"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full mb-4 p-3 border rounded-md"
                />
                <input
                    type="date"
                    name="fecha_nacimiento"
                    value={formData.fecha_nacimiento}
                    onChange={handleChange}
                    required
                    className="w-full mb-4 p-3 border rounded-md"
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Contraseña"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    className="w-full mb-4 p-3 border rounded-md"
                />
                <input
                    type="password"
                    name="confirm"
                    placeholder="Confirmar contraseña"
                    value={formData.confirm}
                    onChange={handleChange}
                    required
                    className="w-full mb-6 p-3 border rounded-md"
                />

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 transition font-semibold"
                >
                    {loading ? "Registrando..." : "Registrarse"}
                </button>
            </form>
        </div>
    );
}
