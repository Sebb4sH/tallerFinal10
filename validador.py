from abc import ABC, abstractmethod
import re
import errores  

class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada):
        self._longitud_esperada = longitud_esperada

    def _validar_longitud(self, clave):
        if len(clave) <= self._longitud_esperada:
            raise errores.LongitudInvalidaError("La clave no cumple con la longitud mínima requerida.")
        return True

    def _contiene_mayuscula(self, clave):
        if not any(c.isupper() for c in clave):
            raise errores.MayusculaInvalidaError("La clave debe contener al menos una letra mayúscula.")
        return True

    def _contiene_minuscula(self, clave):
        if not any(c.islower() for c in clave):
            raise errores.MinusculaInvalidaError("La clave debe contener al menos una letra minúscula.")
        return True

    def _contiene_numero(self, clave):
        if not any(c.isdigit() for c in clave):
            raise errores.NumeroInvalidoError("La clave debe contener al menos un número.")
        return True

    @abstractmethod
    def es_valida(self, clave):
        pass

class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self):
        super().__init__(8)

    def _contiene_caracter_especial(self, clave):
        if not any(c in "@_#$%" for c in clave):
            raise errores.CaracterEspecialInvalidoError("La clave debe contener al menos un caracter especial (@, _, #, $, %).")
        return True

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self._contiene_caracter_especial(clave)
        return True

class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self):
        super().__init__(6)

    def _contiene_calisto(self, clave):
        pos = clave.lower().find("calisto")
        if pos == -1:
            raise errores.CalistoInvalidoError("La clave debe contener la palabra 'calisto'.")
        subcadena = clave[pos:pos+7]
        mayusculas = sum(1 for c in subcadena if c.isupper())
        if mayusculas < 2 or mayusculas == len(subcadena):
            raise errores.CalistoMayusculasInvalidoError("La palabra 'calisto' debe contener al menos dos letras mayúsculas, pero no todas.")
        return True

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_numero(clave)
        self._contiene_calisto(clave)
        return True

class Validador:
    def __init__(self, regla):
        self.regla = regla

    def es_valida(self, clave):
        return self.regla.es_valida(clave)
