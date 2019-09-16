from etherpad_lite import EtherpadLiteClient
import plenumconfig as cfg


def main():
    c = EtherpadLiteClient(base_params={'apikey': cfg.myapikey}, base_url=cfg.mybaseURL)
    c.setText(padID=cfg.mypadIDFalse, text=cfg.falsPadText)


if __name__ == "__main__":
    main()