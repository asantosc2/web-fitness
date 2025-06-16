// src/utils/confirmar.ts
import { confirmAlert } from "react-confirm-alert";

export function confirmar(mensaje: string): Promise<boolean> {
  return new Promise((resolve) => {
    confirmAlert({
      title: "Confirmar acción",
      message: mensaje,
      buttons: [
        {
          label: "Sí",
          onClick: () => resolve(true),
        },
        {
          label: "No",
          onClick: () => resolve(false),
        },
      ],
      closeOnEscape: true,
      closeOnClickOutside: true,
      overlayClassName: "overlay-custom",
    });
  });
}
