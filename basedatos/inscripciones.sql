-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3307
-- Tiempo de generación: 08-09-2025 a las 14:54:11
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `inscripciones`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumno`
--

CREATE TABLE `alumno` (
  `IDAlum` int(100) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `edad` int(3) NOT NULL,
  `dni` int(15) NOT NULL,
  `domicilio` varchar(100) NOT NULL,
  `secundario` varchar(50) NOT NULL,
  `repitente` int(50) NOT NULL,
  `anio` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alumno`
--

INSERT INTO `alumno` (`IDAlum`, `nombre`, `apellido`, `edad`, `dni`, `domicilio`, `secundario`, `repitente`, `anio`) VALUES
(1, 'Amulen', 'Gutierrez', 17, 48601791, 'Joaquin.v.gonzales', '0', 0, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripciones`
--

CREATE TABLE `inscripciones` (
  `IDAlum` int(15) NOT NULL,
  `IdTutor` int(11) NOT NULL,
  `IDInscripcion` int(11) NOT NULL,
  `Escuela_procedente` varchar(50) NOT NULL,
  `Curso_ingresante` varchar(15) NOT NULL,
  `Repitente` tinyint(1) NOT NULL,
  `Observaciones` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tutores`
--

CREATE TABLE `tutores` (
  `IDTutor` int(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apelido` varchar(50) NOT NULL,
  `correo electrónico` int(11) NOT NULL,
  `vinculo con estudiante` int(11) NOT NULL,
  `dni` int(11) NOT NULL,
  `numero de telefono` int(11) NOT NULL,
  `barrio` int(11) NOT NULL,
  `domicilio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `mail` varchar(120) NOT NULL,
  `password` varchar(255) NOT NULL,
  `creado_en` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `mail`, `password`, `creado_en`) VALUES
(1, 'Amulen', 'Gutierrez', 'amulengut@gmail.com', 'scrypt:32768:8:1$P17lcHOWTBbmr472$b061a471363cb20b47f1446612705e455a429ee834f3b1e479609eea1359b4104091497d586c2af63cbd535a414b77f9797d783c1f00d2deb8fbed0f9ce94c6d', '2025-09-08 08:36:41');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alumno`
--
ALTER TABLE `alumno`
  ADD PRIMARY KEY (`IDAlum`),
  ADD UNIQUE KEY `ID` (`IDAlum`);

--
-- Indices de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD PRIMARY KEY (`IDInscripcion`),
  ADD UNIQUE KEY `alumn` (`IDAlum`);

--
-- Indices de la tabla `tutores`
--
ALTER TABLE `tutores`
  ADD PRIMARY KEY (`IDTutor`),
  ADD UNIQUE KEY `IDTutor` (`IDTutor`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `mail` (`mail`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alumno`
--
ALTER TABLE `alumno`
  MODIFY `IDAlum` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  MODIFY `IDInscripcion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tutores`
--
ALTER TABLE `tutores`
  MODIFY `IDTutor` int(50) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

