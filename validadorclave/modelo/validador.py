from abc import ABC, abstractmethod
from validadorclave.modelo.errores import (
    NoCumpleLongitudMinimaError,
    NoTieneLetraMayusculaError,
    NoTieneLetraMinusculaError,
    NoTieneNumeroError,
    NoTieneCaracterEspecialError,
    NoTienePalabraSecretaError
)


def _contiene_mayuscula(clave):
    if not any(c.isupper() for c in clave):
        raise NoTieneLetraMayusculaError("La clave debe tener al menos una letra mayúscula")


class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada):
        self._longitud_esperada = longitud_esperada

    @abstractmethod
    def es_valida(self, clave):
        pass

    def _validar_longitud(self, clave):
        if len(clave) <= self._longitud_esperada:
            raise NoCumpleLongitudMinimaError(
                f"La clave debe tener más de {self._longitud_esperada} caracteres"
            )

    def _contiene_minuscula(self, clave):
        if not any(c.islower() for c in clave):
            raise NoTieneLetraMinusculaError("La clave debe tener al menos una letra minúscula")

    def _contiene_numero(self, clave):
        if not any(c.isdigit() for c in clave):
            raise NoTieneNumeroError("La clave debe tener al menos un número")


class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self):
        super().__init__(8)

    def contiene_caracter_especial(self, clave):
        especiales = "@_#$%"
        if not any(c in especiales for c in clave):
            raise NoTieneCaracterEspecialError(
                "La clave debe tener al menos un caracter especial (@, _, #, $, %)"
            )

    def es_valida(self, clave):
        self._validar_longitud(clave)
        _contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self.contiene_caracter_especial(clave)
        return True


class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self):
        super().__init__(6)

    def contiene_calisto(self, clave):
        palabra = "calisto"
        if palabra in clave.lower():
            letras_encontradas = [c for c in clave if c.lower() in palabra]
            mayusculas = [c for c in letras_encontradas if c.isupper()]
            if len(mayusculas) < 2 or len(mayusculas) == len(palabra):
                raise NoTienePalabraSecretaError(
                    "La palabra calisto debe tener al menos dos letras en mayúscula, pero no todas"
                )
        else:
            raise NoTienePalabraSecretaError("La palabra calisto debe estar en la clave")

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_numero(clave)
        self.contiene_calisto(clave)
        return True


class Validador:
    def __init__(self, regla):
        self.regla = regla

    def es_valida(self, clave):
        return self.regla.es_valida(clave)
