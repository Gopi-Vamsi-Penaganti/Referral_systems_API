CREATE TABLE ReferralSystem (
    PhoneNumber varchar(12) NOT NULL PRIMARY KEY,
    FullName varchar(255) NOT NULL,
    ReferralCode varchar(255),
    ReferredNum varchar(255),
    ReferredContacts varchar(255),
    Balance varchar(255)
);