"""Spanish (Costa Rica) locale.

Names are common in Costa Rica; full names carry two surnames
(primer y segundo apellido), as is customary in the country.
"""

from __future__ import annotations

from testseed.locales._base import LocaleData

LOCALE = LocaleData(
    code="es_CR",
    name="Español (Costa Rica)",
    first_names=(
        "María", "Ana", "Laura", "Sofía", "Valeria", "Daniela", "Fernanda",
        "Gabriela", "Andrea", "Carolina", "Mariana", "Natalia", "Paola",
        "Adriana", "Silvia", "Marcela", "Karla", "Melissa", "Rebeca", "Camila",
        "Isabella", "Raquel", "Lucía", "Jimena", "Priscilla", "José", "Juan",
        "Carlos", "Luis", "Andrés", "Diego", "Esteban", "Pablo", "Alejandro",
        "Fabián", "Mauricio", "Sebastián", "Daniel", "Jorge", "Ricardo",
        "Rodrigo", "Gabriel", "Mateo", "Santiago", "Marco", "Óscar", "Javier",
        "Kevin", "Josué", "Adrián",
    ),
    last_names=(
        "Rodríguez", "Vargas", "Jiménez", "Mora", "Rojas", "González",
        "Hernández", "Sánchez", "Ramírez", "Castro", "Solís", "Araya",
        "Alvarado", "Chaves", "Quesada", "Villalobos", "Salazar", "Calderón",
        "Arias", "Brenes", "Campos", "Fernández", "Montero", "Zúñiga",
        "Madrigal", "Ugalde", "Cordero", "Espinoza", "Valverde", "Murillo",
        "Porras", "Badilla", "Carvajal", "Herrera", "Segura", "Umaña",
        "Navarro", "Picado",
    ),
    surnames_per_person=2,
    email_domains=("correo.test", "ejemplo.test", "pruebas.test"),
)  # fmt: skip
