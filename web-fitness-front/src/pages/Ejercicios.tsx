import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

interface Ejercicio {
  id: number;
  nombre: string;
  grupo_muscular: string;
  tipo_equipo: string;
  imagen_url?: string | null;
}

export default function Ejercicios() {
  const { estado } = useAuth();
  const [ejercicios, setEjercicios] = useState<Ejercicio[]>([]);
  const [grupoFiltro, setGrupoFiltro] = useState<string>("");
  const [equipoFiltro, setEquipoFiltro] = useState<string>("");
  const [nombreFiltro, setNombreFiltro] = useState<string>("");
  const navigate = useNavigate();

  const grupos = Array.from(new Set(ejercicios.map(e => e.grupo_muscular)));
  const equipos = Array.from(new Set(ejercicios.map(e => e.tipo_equipo)));

  const ejerciciosOrdenados = [...ejercicios].sort((a, b) =>
    a.nombre.localeCompare(b.nombre)
  );

  const ejerciciosFiltrados = ejerciciosOrdenados.filter(ej =>
    (grupoFiltro === "" || ej.grupo_muscular === grupoFiltro) &&
    (equipoFiltro === "" || ej.tipo_equipo === equipoFiltro) &&
    (nombreFiltro === "" || ej.nombre.toLowerCase().includes(nombreFiltro.toLowerCase()))
  );

  useEffect(() => {
    fetch("http://localhost:8000/ejercicios", {
      headers: {
        Authorization: `Bearer ${estado.token}`,
      },
    })
      .then(res => res.json())
      .then(data => setEjercicios(data))
      .catch(err => console.error("Error cargando ejercicios:", err));
  }, [estado.token]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-100 to-indigo-100 pt-24 px-6">
      <Navbar />
      <h1 className="text-4xl font-bold text-center text-blue-700 mb-10">
        Lista de ejercicios
      </h1>

      <div className="max-w-6xl mx-auto bg-white shadow-md rounded-lg p-6 mb-10 grid grid-cols-1 md:grid-cols-4 gap-4">
        <input
          type="text"
          placeholder="Buscar por nombre"
          value={nombreFiltro}
          onChange={e => setNombreFiltro(e.target.value)}
          className="border px-3 py-2 rounded shadow-sm"
        />
        <select
          value={grupoFiltro}
          onChange={e => setGrupoFiltro(e.target.value)}
          className="border px-3 py-2 rounded shadow-sm"
        >
          <option value="">Todas las partes del cuerpo</option>
          {grupos.map(grupo => (
            <option key={grupo} value={grupo}>{grupo}</option>
          ))}
        </select>

        <select
          value={equipoFiltro}
          onChange={e => setEquipoFiltro(e.target.value)}
          className="border px-3 py-2 rounded shadow-sm"
        >
          <option value="">Todas las categorías</option>
          {equipos.map(equipo => (
            <option key={equipo} value={equipo}>{equipo}</option>
          ))}
        </select>

        <button
          onClick={() => navigate("/ejercicios/nuevo")}
          className="bg-blue-600 text-white font-semibold px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          Añadir ejercicio
        </button>
      </div>

      <div className="max-w-5xl mx-auto flex flex-col gap-4">
        {ejerciciosFiltrados.map(ej => (
          <div
            key={ej.id}
            onClick={() => navigate(`/ejercicios/${ej.id}`)}
            className="cursor-pointer bg-white rounded-xl shadow p-4 flex items-center justify-between hover:shadow-lg hover:bg-gray-50 transition"
          >
            <div className="flex items-center gap-4">
              {ej.imagen_url ? (
                <img
                  src={ej.imagen_url}
                  alt={ej.nombre}
                  className="w-20 h-20 object-cover rounded-md"
                />
              ) : (
                <div className="w-20 h-20 bg-gray-200 flex items-center justify-center rounded-md text-gray-500">
                  Sin imagen
                </div>
              )}
              <div>
                <h2 className="text-xl font-semibold text-gray-800">{ej.nombre}</h2>
                <p className="text-sm text-gray-500 capitalize">{ej.grupo_muscular}</p>
              </div>
            </div>
            <div className="text-sm text-gray-500 pr-4">
              <span className="font-medium text-gray-700">Equipo:</span> {ej.tipo_equipo}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
