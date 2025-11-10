-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3307
-- Tiempo de generación: 10-11-2025 a las 12:35:50
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
  `secundario_cursado` varchar(50) NOT NULL,
  `repitente` int(50) NOT NULL,
  `anio_cursado` int(50) NOT NULL,
  `fecha_inscripcion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alumno`
--

INSERT INTO `alumno` (`IDAlum`, `nombre`, `apellido`, `edad`, `dni`, `domicilio`, `secundario_cursado`, `repitente`, `anio_cursado`, `fecha_inscripcion`) VALUES
(33, 'amulen', 'Gutierrez', 16, 48074456, 'Joaquin.V.Gonzales 348', '', 0, 0, '2025-10-20 08:41:22'),
(34, 'Viviana', 'Guillen', 12, 45555555, 'Joaquin.V.Gonzales 348', '', 0, 0, '2025-10-20 08:43:26'),
(35, 'Amulen', 'Gutierrez', 17, 4555555, 'Joaquin.V.Gonzales 348', '', 0, 0, '2025-10-22 16:26:17'),
(36, 'Amulen', 'Gutierrez', 17, 4555554, 'Joaquin.V.Gonzales 348', '', 0, 0, '2025-11-05 13:19:00'),
(37, 'Pedro', 'Perez', 15, 50222222, 'libertad y alberdi', '', 0, 0, '2025-11-10 08:24:49'),
(38, 'Pedro', 'Perez', 15, 50300400, 'libertad y alberdi', '', 0, 0, '2025-11-10 08:29:47');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripciones`
--

CREATE TABLE `inscripciones` (
  `IDAlum` int(15) NOT NULL,
  `IdTutor` int(11) NOT NULL,
  `IDInscripcion` int(11) NOT NULL,
  `fecha_inscripcion` datetime NOT NULL,
  `Escuela_procedente` varchar(50) NOT NULL,
  `Curso_ingresante` varchar(15) NOT NULL,
  `Repitente` varchar(15) NOT NULL,
  `Observaciones` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inscripciones`
--

INSERT INTO `inscripciones` (`IDAlum`, `IdTutor`, `IDInscripcion`, `fecha_inscripcion`, `Escuela_procedente`, `Curso_ingresante`, `Repitente`, `Observaciones`) VALUES
(33, 29, 22, '2025-10-20 08:41:22', 'PRoA Rio Tercero', '4ª', 'No', ''),
(34, 30, 23, '2025-10-20 08:43:27', 'IPEM 288', '4ª', 'No', 'me'),
(35, 31, 24, '2025-10-22 16:26:17', 'IPEM 288', '4ª', 'No', ''),
(36, 32, 25, '2025-11-05 13:19:00', 'IPEM 288', '4ª', 'No', ''),
(37, 33, 26, '2025-11-10 08:24:49', 'IPEM 288', '4ª', 'si. 3', 'no se'),
(38, 34, 27, '2025-11-10 08:29:47', 'IPEM 288', '4ª', 'si. 3', '');

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
  `domicilio` int(11) NOT NULL,
  `estudiante_id` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefono` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tutores`
--

INSERT INTO `tutores` (`IDTutor`, `nombre`, `apelido`, `correo electrónico`, `vinculo con estudiante`, `dni`, `numero de telefono`, `barrio`, `domicilio`, `estudiante_id`, `email`, `telefono`) VALUES
(29, 'facu Gutierrez', '', 0, 0, 60014521, 0, 0, 0, 33, 'amulengut@gmail.com', '03571360006'),
(30, 'facu Guillen', '', 0, 0, 60014521, 0, 0, 0, 34, 'amulengut@gmail.com', '03571360006'),
(31, 'facu Guillen', '', 0, 0, 60014521, 0, 0, 0, 35, 'amulengut@gmail.com', '03571360006'),
(32, 'facu Guillen', '', 0, 0, 60014521, 0, 0, 0, 36, 'amulengut@gmail.com', '03571360006'),
(33, '', '', 0, 0, 0, 0, 0, 0, 37, '', ''),
(34, 'Andrea Perez', '', 0, 0, 25587456, 0, 0, 0, 38, 'aperez@gmail.com', '3571500800');

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
(1, 'Amulen', 'Gutierrez', 'amulengut@gmail.com', 'scrypt:32768:8:1$P17lcHOWTBbmr472$b061a471363cb20b47f1446612705e455a429ee834f3b1e479609eea1359b4104091497d586c2af63cbd535a414b77f9797d783c1f00d2deb8fbed0f9ce94c6d', '2025-09-08 08:36:41'),
(3, 'usuario', 'administrador', 'admin123@gmail.com', 'scrypt:32768:8:1$NA4S9qTAcw4r4D84$06c996a5dc89aa3a9fb78e0e61905e512a0696c31b5c0d2088dc720a77a78463be319cbc12a2b3975a3e7cb85171890f4e4eb5facd829276d5cf791bbf588134', '2025-10-27 08:26:44'),
(4, 'Andrea', 'Perez', 'aperez@gmail.com', 'scrypt:32768:8:1$qc4DGb8mO3oQHS3T$3c3816bec13d169f8302360a65fe727fbc3632da6d4b53d6d087141d13a0b1ebc5fcbf0371028ad2188e66f453a69de4a863426a833f80844871defc80386847', '2025-11-10 08:28:35');

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
  ADD UNIQUE KEY `IDTutor` (`IDTutor`),
  ADD KEY `fk_estudiante` (`estudiante_id`);

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
  MODIFY `IDAlum` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  MODIFY `IDInscripcion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `tutores`
--
ALTER TABLE `tutores`
  MODIFY `IDTutor` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tutores`
--
ALTER TABLE `tutores`
  ADD CONSTRAINT `fk_estudiante` FOREIGN KEY (`estudiante_id`) REFERENCES `alumno` (`IDAlum`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
