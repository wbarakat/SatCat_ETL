import configparser
import sys
import pathlib
import datetime
import requests
import pandas as pd

# read variables from config file
parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.resolve()
config_file = "configuration.conf"
parser.read(f"{script_path}/{config_file}")

configUsr = parser.get("startracker_config", "username")
configPwd = parser.get("startracker_config", "password")
siteCred = {"identity": configUsr, "password": configPwd}

# URI and paths for database we are interested in getting
URI_BASE = "https://www.space-track.org"
REQUEST_LOGIN = "/ajaxauth/login"
REQUEST_DB = "/basicspacedata/query/class/satcat/predicates"


def main():
    api_json = connect_api()
    raw_data = convert_json_to_df(api_json)
    final_data = transform_data(raw_data)
    download_to_csv(final_data)



def connect_api() -> list:
    try:
        # use requests package to drive the RESTful session with space-track.org
        with requests.Session() as session:
            # run the session in a with block to force session to close if we exi
            resp = session.post(URI_BASE + REQUEST_LOGIN, data=siteCred)
            resp = session.get(URI_BASE + REQUEST_DB)
            data = resp.json()
            session.close()
        return data
    except Exception as e:
        print(f"Unable to connect to API: {e}")
        sys.exit(1)


def convert_json_to_df(api_json) -> pd.DataFrame:
    # convert json to pandas dataframe
    df = pd.json_normalize(api_json)
    return df


def transform_data(raw_data) -> pd.DataFrame:
    # drop unwanted columns
    columns_to_drop = [
        "INTLDES",
        "COMMENT",
        "COMMENTCODE",
        "RCSVALUE",
        "RCS_SIZE",
        "FILE",
        "LAUNCH_NUM",
        "LAUNCH_PIECE",
        "CURRENT",
        "OBJECT_NAME",
        "OBJECT_ID",
        "OBJECT_NUMBER",
    ]
    df = raw_data.drop(columns_to_drop, 1)

    # calculate lifespan of satellite based on launch and decay year
    df["LAUNCH"] = pd.to_datetime(df["LAUNCH"])
    df["DECAY"] = pd.to_datetime(df["DECAY"])
    df["LIFESPAN_DAYS"] = (
        df["DECAY"].fillna(datetime.datetime.today()) - df["LAUNCH"]
    ).dt.days

    # convert to appropriate datatypes
    df = df.convert_dtypes()

    # convert float columns
    columns_to_convert = ["PERIOD", "INCLINATION", "APOGEE", "PERIGEE"]
    df[columns_to_convert] = df[columns_to_convert].apply(
        pd.to_numeric, errors="coerce", axis=1
    )

    # convert integer columns
    df["NORAD_CAT_ID"] = df["NORAD_CAT_ID"].astype(int)
    #df["LAUNCH_YEAR"] = df["LAUNCH_YEAR"].astype(int)

    return df


def download_to_csv(final_data) -> None:
    final_data.to_csv("/tmp/spacetracker_satcat_data.csv", index=False)


if __name__ == "__main__":
    main()
