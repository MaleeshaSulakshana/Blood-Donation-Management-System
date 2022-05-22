-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 22, 2022 at 12:19 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 7.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `blood_donation`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins_details`
--

CREATE TABLE `admins_details` (
  `id` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admins_details`
--

INSERT INTO `admins_details` (`id`, `email`, `name`) VALUES
(1, 'maleeshaa@gmail.com', 'Maleesha Sulakshana'),
(3, 'thenukaa@gmail.com', 'Thenuka');

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(255) NOT NULL,
  `campaign_id` int(255) NOT NULL,
  `donor` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `campaign_id`, `donor`) VALUES
(4, 2147483647, 'maleesha@gmail.com'),
(5, 2147482984, 'maleesha@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `campaigns`
--

CREATE TABLE `campaigns` (
  `id` int(255) NOT NULL,
  `campaign_id` int(255) NOT NULL,
  `organization_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `venue` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `start_time` varchar(255) NOT NULL,
  `end_time` varchar(255) NOT NULL,
  `lat` varchar(255) NOT NULL,
  `lon` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `thumbnail` varchar(255) NOT NULL,
  `is_approved` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `campaigns`
--

INSERT INTO `campaigns` (`id`, `campaign_id`, `organization_id`, `name`, `venue`, `date`, `start_time`, `end_time`, `lat`, `lon`, `description`, `thumbnail`, `is_approved`) VALUES
(1, 2147483647, 'thenukao@gmail.com', 'NSBM Campaign - Scool Junction', 'NSBM', '2022-05-17', '09:32', '21:32', '6.82388511775028', '80.03042228359134', 'hello', '20220329713254..jpg', 1),
(2, 2147483612, 'thenukao@gmail.com', 'NSBM Campaign', 'NSBM', '2022-06-02', '09:32', '21:32', '6.822053495992932', '80.0415729', 'hello', '20220329493561..jpg', 0),
(3, 2147482984, 'thenukao@gmail.com', 'NSBM Campaign - Temple Junction', 'NSBM', '2022-06-05', '09:32', '21:32', '6.828327908029834', '80.02655709708472', 'hello', '20220329493524..jpg', 1);

-- --------------------------------------------------------

--
-- Table structure for table `donations`
--

CREATE TABLE `donations` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `amount` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL,
  `payment_id` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `donations`
--

INSERT INTO `donations` (`id`, `name`, `email`, `amount`, `date`, `payment_id`) VALUES
(1, 'Thenuka', 'thenuka@gmail.com', '20', '2022-04-27', 'PAYID-MJUGKLQ5X24957133865951N');

-- --------------------------------------------------------

--
-- Table structure for table `donation_details`
--

CREATE TABLE `donation_details` (
  `id` int(255) NOT NULL,
  `donor_email` varchar(255) NOT NULL,
  `campaign_id` int(255) NOT NULL,
  `units` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `donation_details`
--

INSERT INTO `donation_details` (`id`, `donor_email`, `campaign_id`, `units`) VALUES
(1, 'maleesha@gmail.com', 2147483647, 1);

-- --------------------------------------------------------

--
-- Table structure for table `emergency_needs`
--

CREATE TABLE `emergency_needs` (
  `id` int(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `description` varchar(3000) NOT NULL,
  `hospital_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `emergency_needs`
--

INSERT INTO `emergency_needs` (`id`, `title`, `date`, `description`, `hospital_id`) VALUES
(2, 'AB+ Kidney', '2022-05-18', 'We want AB+ Kidney immediately.', 'asirihospital@gmail.com'),
(3, 'B+ Kidney', '2022-05-18', 'We want B+ Kidney immediately.', 'asirihospital@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `hospitals_details`
--

CREATE TABLE `hospitals_details` (
  `id` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `number` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hospitals_details`
--

INSERT INTO `hospitals_details` (`id`, `email`, `name`, `address`, `number`) VALUES
(2, 'asirihospital@gmail.com', 'Asiri Hospital Colombo', 'Asiri Hospital, Colombo', '0112456235');

-- --------------------------------------------------------

--
-- Table structure for table `organizations_details`
--

CREATE TABLE `organizations_details` (
  `id` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `hod` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `number` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `organizations_details`
--

INSERT INTO `organizations_details` (`id`, `email`, `name`, `hod`, `location`, `number`) VALUES
(1, 'maleeshao@gmail.com', 'Mr Jayasinghe, M P M S', 'Maleesha', 'Homagama', '0767950600'),
(2, 'sulakshanao@gmail.com', 'Mr Sulakshana Organization', 'Sulakshana', 'Homagama', '0767950600'),
(3, 'thenukao@gmail.com', 'Thenuka Organization', 'Thenuka', 'Homagama', '0764572695');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `psw` varchar(255) NOT NULL,
  `account_type` varchar(255) NOT NULL,
  `is_approved` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `psw`, `account_type`, `is_approved`) VALUES
(3, 'maleesha@gmail.com', '25d55ad283aa400af464c76d713c07ad', '4', 1),
(7, 'maleeshao@gmail.com', '25d55ad283aa400af464c76d713c07ad', '2', 1),
(8, 'maleeshaa@gmail.com', '25d55ad283aa400af464c76d713c07ad', '1', 1),
(9, 'sulakshana@gmail.com', '041ad8577c21260a7b915ee08bfa5e4b', '4', 0),
(10, 'sulakshanao@gmail.com', '25d55ad283aa400af464c76d713c07ad', '2', 1),
(12, 'thenukaa@gmail.com', '25d55ad283aa400af464c76d713c07ad', '1', 1),
(13, 'thenuka@gmail.com', '041ad8577c21260a7b915ee08bfa5e4b', '4', 1),
(14, 'thenukao@gmail.com', '25d55ad283aa400af464c76d713c07ad', '2', 1),
(17, 'asirihospital@gmail.com', '25d55ad283aa400af464c76d713c07ad', '3', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users_details`
--

CREATE TABLE `users_details` (
  `id` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `dob` varchar(255) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `blood_type` varchar(255) NOT NULL,
  `phone_number` varchar(255) NOT NULL,
  `nic` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users_details`
--

INSERT INTO `users_details` (`id`, `email`, `full_name`, `dob`, `gender`, `blood_type`, `phone_number`, `nic`) VALUES
(1, 'maleesha@gmail.com', 'Maleesha Sulakshana', '1998-10-02', 'Male', 'AB+', '0767950600', '982870837V'),
(2, 'sulakshana@gmail.com', 'Maleesha Sulakshana', '1998-10-02', 'Male', 'AB+', '0767950600', '982870837V'),
(3, 'thenuka@gmail.com', 'Thenuka', '1998-10-02', 'Male', 'AB+', '0767953856', '982870837V');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins_details`
--
ALTER TABLE `admins_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `campaigns`
--
ALTER TABLE `campaigns`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `donations`
--
ALTER TABLE `donations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `donation_details`
--
ALTER TABLE `donation_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `emergency_needs`
--
ALTER TABLE `emergency_needs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hospitals_details`
--
ALTER TABLE `hospitals_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `organizations_details`
--
ALTER TABLE `organizations_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users_details`
--
ALTER TABLE `users_details`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins_details`
--
ALTER TABLE `admins_details`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `campaigns`
--
ALTER TABLE `campaigns`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `donations`
--
ALTER TABLE `donations`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `donation_details`
--
ALTER TABLE `donation_details`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `emergency_needs`
--
ALTER TABLE `emergency_needs`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `hospitals_details`
--
ALTER TABLE `hospitals_details`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `organizations_details`
--
ALTER TABLE `organizations_details`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `users_details`
--
ALTER TABLE `users_details`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
