-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 01, 2018 at 07:38 PM
-- Server version: 5.7.17
-- PHP Version: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `biblestu_dy`
--

-- --------------------------------------------------------

--
-- Table structure for table `verses`
--

DROP TABLE IF EXISTS `verses`;
CREATE TABLE `verses` (
  `verseID` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `bookCode` varchar(3) NOT NULL,
  `chapter` smallint(4) NOT NULL,
  `verseNumber` smallint(4) NOT NULL,
  `verseText` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `verses`
--

INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) VALUES
('GEN',   1,   1, 'In the beginning, God<H0430> created the heavens and the earth.'),
('GEN',   1,   2, 'The earth was formless and empty. Darkness was on the surface of the deep and God<H0430>\'s Spirit was hovering over the surface of the waters.'),
('GEN',   1,   3, 'God<H0430> said, \"Light is!\" and there was light.'),
('GEN',   1,   4, 'God<H0430> saw the light, and saw that it was good. God<H0430> divided the light from the darkness.'),
('GEN',   1,   5, 'God<H0430> called the light \"day,\" and he called the darkness \"night\". There was evening and there was morning, day one.'),
('GEN',   1,   6, 'God<H0430> said, \"There is an expanse in the middle of the waters, and it divides the waters from the waters.\"'),
('GEN',   1,   7, 'God<H0430> made the expanse, and divided the waters which were under the expanse from the waters which were above the expanse; and it was so.'),
('GEN',   1,   8, 'God<H0430> called the expanse \"sky\". There was evening and there was morning, day two.'),
('GEN',   1,   9, 'God<H0430> said, \"The waters under the sky are gathered together to one place, and dry land appears;\" and it was so.'),
('GEN',   1,  10, 'God<H0430> called the dry land \"earth\", and he called the gathering together of the waters \"seas\". God<H0430> saw that it was good.'),
('GEN',   1,  11, 'God<H0430> said, \"The earth sprouts grass and plants<H6212> yielding seeds, and fruit trees bearing fruit after their kind, with their seeds in them, on the earth;\" and it was so.'),
('GEN',   1,  12, 'The earth produced grass and plants<H6212> yielding seed after their kind, and trees bearing fruit, with their seeds in them, after their kind; and God<H0430> saw that it was good.'),
('GEN',   1,  13, 'There was evening and there was morning, day three.'),
('GEN',   1,  14, 'God<H0430> said, \"There are lights in the expanse of sky to divide the day from the night; and they are for signs to mark seasons, days, and years;'),
('GEN',   1,  15, 'and they are for lights in the expanse of sky to give light on the earth;\" and it was so.'),
('GEN',   1,  16, 'God<H0430> made the two great lights: the greater light to rule the day, and the lesser light to rule the night. He also made the stars.'),
('GEN',   1,  17, 'God<H0430> set them in the expanse of sky to give light to the earth,'),
('GEN',   1,  18, 'and to rule over the day and over the night, and to divide the light from the darkness. God<H0430> saw that it was good.'),
('GEN',   1,  19, 'There was evening and there was morning, day four.'),
('GEN',   1,  20, 'God<H0430> said, \"The waters abound with swarms of living creatures, and birds fly above the earth in the open expanse of sky.\"'),
('GEN',   1,  21, 'God<H0430> created the large sea creatures and every living creature that moves, with which the waters swarmed, after their kind, and every winged bird after its kind. God<H0430> saw that it was good.'),
('GEN',   1,  22, 'God<H0430> blessed them, saying, \"Be fruitful, and multiply, and fill the waters in the seas, and let birds multiply on the earth.\"'),
('GEN',   1,  23, 'There was evening and there was morning, day five.'),
('GEN',   1,  24, 'God<H0430> said, \"The earth produces living creatures after their kind, livestock, creeping things, and animals of the earth after their kind;\" and it was so.'),
('GEN',   1,  25, 'God<H0430> made the animals of the earth after their kind, and the livestock after their kind, and everything that creeps on the ground after its kind. God<H0430> saw that it was good.'),
('GEN',   1,  26, 'God<H0430> said, \"We make mankind in our image, after our likeness. Let them have dominion over the fish of the sea, and over the birds of the sky, and over the livestock, and over all the earth, and over every creeping thing that creeps on the earth.\"'),
('GEN',   1,  27, 'God<H0430> created mankind in his own image. In God<H0430>\'s image he created them; male and female he created them.'),
('GEN',   1,  28, 'God<H0430> blessed them. God<H0430> said to them, \"Be fruitful, multiply, fill the earth, and subdue it. Have dominion over the fish of the sea, over the birds of the sky, and over every living thing that moves on the earth.\"'),
('GEN',   1,  29, 'God<H0430> said, \"Behold, I have given you every plant<H6212> yielding seed, which is on the surface of all the earth, and every tree, which bears fruit yielding seed. It will be your food.'),
('GEN',   1,  30, 'To every animal of the earth, and to every bird of the sky, and to everything that creeps on the earth, in which there is life, I have given every green plant<H6212> for food;\" and it was so.'),
('GEN',   1,  31, 'God<H0430> saw everything that he had made, and, behold, it was very good. There was evening and there was morning, day six.'),
('GEN',   2,   1, 'The heavens, the earth, and all their vast array were finished.'),
('GEN',   2,   2, 'On day seven God<H0430> finished the work he\'d done; and he rested on day seven from all the work he\'d done.'),
('GEN',   2,   3, 'God<H0430> blessed the seventh day, and made it holy, because he rested in it from all the work of creation which he\'d done.'),
('GEN',   2,   4, 'This is the history of the generations of the heavens and of the earth when they were created, in the day that TheIAM<H3068> God<H0430> made the earth and the heavens.'),
('GEN',   2,   5, 'No plant of the field was yet in the earth, and no vegetation<H6212> of the field had yet sprung up; for TheIAM<H3068> God<H0430> had not caused it to rain on the earth. There was not a man to till the ground,'),
('GEN',   2,   6, 'but a mist went up from the earth, and watered the whole surface of the ground.'),
('GEN',   2,   7, 'TheIAM<H3068> God<H0430> formed man from the dust of the ground, and breathed into his nostrils the breath of life; and man became a living soul.'),
('GEN',   2,   8, 'TheIAM<H3068> God<H0430> planted a garden eastward, in Eden, and there he put the man whom he had formed.'),
('GEN',   2,   9, 'Out of the ground TheIAM<H3068> God<H0430> made every tree to grow that is pleasant to the sight, and good for food, including the tree of life in the middle of the garden and the tree of the knowledge of good and evil.'),
('GEN',   2,  10, 'A river went out of Eden to water the garden; and from there it was parted, and became the source of four rivers.'),
('GEN',   2,  11, 'The name of the first is Pishon which flows through the whole land of Havilah, where there is gold;'),
('GEN',   2,  12, 'and the gold of that land is good. Bdellium and onyx stone are also there.'),
('GEN',   2,  13, 'The name of the second river is Gihon. It is the same river that flows through the whole land of Cush.'),
('GEN',   2,  14, 'The name of the third river is Hiddekel. This is the one which flows in front of Assyria. The fourth river is the Euphrates.'),
('GEN',   2,  15, 'TheIAM<H3068> God<H0430> took the man, and put him into the garden of Eden to cultivate and keep it.'),
('GEN',   2,  16, 'TheIAM<H3068> God<H0430> commanded the man, saying, \"You may freely eat of every tree of the garden;'),
('GEN',   2,  17, 'but you shall not eat of the tree of the knowledge of good and evil; for in the day that you eat of it, you will really die.\"'),
('GEN',   2,  18, 'TheIAM<H3068> God<H0430> said, \"It is not good for the man to be alone. I will make a helper suitable for him.\"'),
('GEN',   2,  19, 'Out of the ground TheIAM<H3068> God<H0430> formed every animal of the field, and every bird of the sky, and brought them to the man to see what he would call them. Whatever the man called every living creature, that was its name.'),
('GEN',   2,  20, 'The man gave names to all livestock, and to the birds of the sky, and to every animal of the field; but for man there was not found a helper suitable for him.'),
('GEN',   2,  21, 'TheIAM<H3068> God<H0430> caused the man to fall into a deep sleep. As the man slept, he took one of his ribs, and closed up the flesh in its place.'),
('GEN',   2,  22, 'TheIAM<H3068> God<H0430> made a woman from the rib which he had taken from the man, and brought her to the man.'),
('GEN',   2,  23, 'The man said, \"This is now bone of my bones, and flesh of my flesh. She will be called \'woman,\' because she was taken out of Man.\"'),
('GEN',   2,  24, 'Therefore a man will leave his father and his mother, and will join with his wife, and they will be one flesh.'),
('GEN',   2,  25, 'The man and the woman were both naked, and they were not ashamed.'),
('GEN',   3,   1, 'Now the serpent was more subtle than any animal of the field which TheIAM<H3068> God<H0430> had made. He said to the woman, \"Has God<H0430> really said, \'You shall not eat of any tree of the garden\'?\"'),
('GEN',   3,   2, 'The woman said to the serpent, \"We may eat fruit from the trees of the garden,'),
('GEN',   3,   3, 'but not the fruit of the tree which is in the middle of the garden. God<H0430> said, \'You shall not eat of it nor touch it, lest you die.\'\"'),
('GEN',   3,   4, 'The serpent said to the woman, \"You won\'t really die,'),
('GEN',   3,   5, 'for God<H0430> knows that in the day you eat it, your eyes will be opened, and you will be like God<H0430>, knowing good and evil.\"'),
('GEN',   3,   6, 'When the woman saw that the tree was good for food, and that it was a delight to the eyes, and that the tree was to be desired to make one wise, she took some of its fruit, and ate; and she gave some to her husband with her, and he ate it, too.'),
('GEN',   3,   7, 'Their eyes were opened, and they both knew that they were naked. They sewed fig leaves together, and made coverings for themselves.'),
('GEN',   3,   8, 'They heard the voice of TheIAM<H3068> God<H0430> walking in the garden in the cool of the day, and the man and his wife hid themselves from the presence of TheIAM<H3068> God<H0430> among the trees of the garden.'),
('GEN',   3,   9, 'TheIAM<H3068> God<H0430> called to the man, and said to him, \"Where are you?\"'),
('GEN',   3,  10, 'The man said, \"I heard your voice in the garden, and I was afraid, because I was naked; so I hid myself.\"'),
