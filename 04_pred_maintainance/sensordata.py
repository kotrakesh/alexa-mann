import time
import json
import config
import pymysql
from flask import Flask, render_template,Response
import Adafruit_GPIO.SPI as SPI# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_MCP3008
app = Flask(__name__)

@app.route("/sensordata")
def sesnordata():
        # Software SPI configuration:
        CLK  = 18
        MISO = 23
        MOSI = 24
        CS   = 25
        mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
        print('Reading MCP3008 values, press Ctrl-C to quit...')
        # Print nice channel column headers.
        # Hardware SPI configuration:
        # SPI_PORT   = 0
        # SPI_DEVICE = 0
        # mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
        values = [0]*8
        for i in range(8):
            # The read_adc function will get the value of the specified channel (0-7).
            values[i] = mcp.read_adc(i)
        jsondata  = json.dumps(values)   
        return Response(jsondata, mimetype='application/json')

if __name__ == "__main__":
	app.run(debug=True)