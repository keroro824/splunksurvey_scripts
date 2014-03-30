DROP TABLE IF EXISTS Questions;
DROP TABLE IF EXISTS QuestionOptions;
DROP TABLE IF EXISTS Responses;
DROP TABLE IF EXISTS Respondents;
DROP TABLE IF EXISTS ResponsesText ;
DROP TABLE IF EXISTS OptionLabel;

CREATE TABLE Questions(
	QuestionID INT,
	PageID INT,
	Position INT,
	QType INT,
	Heading VARCHAR(255),
	PRIMARY KEY (QuestionID)
);

CREATE TABLE QuestionOptions(
	OptionID INT,
	OptionType INT,
	OptionNum INT,
	QuestionID INT,
	OptionText VARCHAR(255),
	PRIMARY KEY (OptionID),
	FOREIGN KEY (QuestionID)
		REFERENCES Questions(QuestionID)
);

CREATE TABLE Responses(
	RespondentID INT,
	CollectorID INT,
	QuestionID INT,
	Key1 INT,
	Key2 INT,
	Key3 INT,
	DateAdded TIMESTAMP,
	FOREIGN KEY (RespondentID)
		REFERENCES Respondents(RespondentID),
	FOREIGN KEY (QuestionID)
		REFERENCES Questions(QuestionID)	
);

CREATE TABLE Respondents(
	RespondentID INT,
	CollectorID INT,
	IPAddress VARCHAR(255),
	Email VARCHAR(255),
	FirstName VARCHAR(255),
	LastName VARCHAR(255),
	CustomData VARCHAR(255),
	DateAdded TIMESTAMP,
	PRIMARY KEY (RespondentID)
);

CREATE TABLE ResponsesText(
	RespondentID INT,
	CollectorID INT,
	QuestionID INT,
	Key1 INT,
	ResponsesText VARCHAR(255),
	DateAdded TIMESTAMP,
	FOREIGN KEY (RespondentID)
		REFERENCES Respondents(RespondentID),
	FOREIGN KEY (QuestionID)
		REFERENCES Questions(QuestionID),
	FOREIGN KEY (Key1)
		REFERENCES QuestionOptions(OptionID)
);

CREATE TABLE OptionLabel(
	OptionID INT,
	OptionLabel TEXT
);
