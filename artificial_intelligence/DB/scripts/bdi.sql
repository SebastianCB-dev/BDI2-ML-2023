
CREATE TABLE "bdi" (
	username VARCHAR(255) PRIMARY KEY,
	sadness INTEGER NULL CHECK (sadness IN (NULL, 0, 1, 2, 3)),
	pessimism INTEGER CHECK (pessimism IN (0, 1, 2, 3)),
	failure INTEGER CHECK (failure IN (0, 1, 2, 3)),
	loss_of_pleasure INTEGER CHECK (loss_of_pleasure IN (0, 1, 2, 3)),
	guilt INTEGER CHECK (guilt IN (0, 1, 2, 3)),
	feeling_of_punishment INTEGER CHECK (feeling_of_punishment IN (0, 1, 2, 3)),
	dissatisfaction_with_oneself INTEGER CHECK (dissatisfaction_with_oneself IN (0, 1, 2, 3)),
	self_criticism INTEGER CHECK (self_criticism IN (0, 1, 2, 3)),
	thoughts_or_wishes_of_death INTEGER CHECK (thoughts_or_wishes_of_death IN (0, 1, 2, 3)),
	crying INTEGER CHECK (crying IN (0, 1, 2, 3)),
	agitation INTEGER CHECK (agitation IN (0, 1, 2, 3)),
	loss_of_interest INTEGER CHECK (loss_of_interest IN (0, 1, 2, 3)),
	indecisiveness INTEGER CHECK (indecisiveness IN (0, 1, 2, 3)),
	devaluation INTEGER CHECK (devaluation IN (0, 1, 2, 3)),
	loss_of_energy INTEGER CHECK (loss_of_energy IN (0, 1, 2, 3)),
	changes_in_sleep_habits INTEGER CHECK (changes_in_sleep_habits IN (0, 1, 2, 3)),
	irritability INTEGER CHECK (irritability IN (0, 1, 2, 3)),
	changes_in_appetite INTEGER CHECK (changes_in_appetite IN (0, 1, 2, 3)),
	difficulty_concentrating INTEGER CHECK (difficulty_concentrating IN (0, 1, 2, 3)),
	tiredness INTEGER CHECK (tiredness IN (0, 1, 2, 3)),
	loss_of_interest_in_sex INTEGER CHECK (loss_of_interest_in_sex IN (0, 1, 2, 3)),
	class INTEGER CHECK (class IN (0, 1))
);

COMMENT ON TABLE "bdi" IS 'Table that stores the users bdi records';
COMMENT ON COLUMN "bdi".username IS 'Username of the user';
COMMENT ON COLUMN "bdi".class IS 'Class of the user where 1 indicates that the user is depressed and 0 indicates that the user is not depressed.';

CREATE INDEX idx_bdi_username ON "bdi" (username);

COMMENT ON INDEX idx_bdi_username IS 'Index on the "username" column to improve query performance';

SELECT * FROM "bdi";