import datetime
import sys
from pathlib import Path

from calenderCalc.iCal import PregnancyICal

def main():
	# presentday = datetime.datetime.today()
	# presentday = presentday.replace(hour=0, minute=0, second=0, microsecond=0)
	# tomorrow = presentday + datetime.timedelta(1)
	# cal = iCal()
	# cal.addEvent(date = tomorrow, name= "Test")
	# cal.writeFile(directory = Path.home() / "Downloads", fileName='Test')
	
	cal = PregnancyICal(lastMonthlyPeriod=datetime.datetime(year=2023, month=12, day=12))
	cal.write(directory = Path.home() / "Downloads")
	

if __name__ == '__main__':
	sys.exit(main())  # pragma: no cover
