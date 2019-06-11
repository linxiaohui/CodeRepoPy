CREATE TABLE institutions(
  AOI_ID TEXT,
  AOI_NAME TEXT,
  PR_COUNT_PERSON TEXT,
  PTI0PERSON TEXT,
  PTI1PERSON TEXT,
  PTI2PERSON TEXT,
  PTI3PERSON TEXT,
  PTI4PERSON TEXT,
  PTI5PERSON TEXT,
  PTI6PERSON TEXT,
  PTI7PERSON TEXT,
  OTC_ID TEXT,
  OTC_NAME TEXT,
  SYNC_STATUS INT
);

CREATE TABLE "institution_type" (
"OTC_DESC" TEXT,
  "OTC_ID" TEXT,
  "OTC_NAME" TEXT
);

CREATE TABLE "person_info" (
"ADI_ID" TEXT,
  "ADI_NAME" TEXT,
  "AOI_ID" TEXT,
  "AOI_NAME" TEXT,
  "ARRIVE_DATE" TEXT,
  "CERTC_ID" TEXT,
  "CERTC_NAME" TEXT,
  "CER_NUM" TEXT,
  "ECO_NAME" TEXT,
  "OBTAIN_DATE" TEXT,
  "PTI_NAME" TEXT,
  "RPI_NAME" TEXT,
  "RPI_PHOTO_PATH" TEXT,
  "SCO_NAME" TEXT,
  "IMAGE_DATA" TEXT
);

CREATE TABLE "stuffs" (
"AOI_NAME" TEXT,
  "CER_NUM" TEXT,
  "COUNTCER" TEXT,
  "COUNTCX" TEXT,
  "CTI_NAME" TEXT,
  "ECO_NAME" TEXT,
  "PPP_END_DATE" TEXT,
  "PPP_GET_DATE" TEXT,
  "PPP_ID" TEXT,
  "PTI_NAME" TEXT,
  "RNUM" INTEGER,
  "RPI_NAME" TEXT,
  "SCO_NAME" TEXT,
  "REC_TIME" TIMESTAMP,
  "OFF_TIME" TIMESTAMP,
  "STATUS" INTEGER,
  "AOI_ID" INTEGER
);
