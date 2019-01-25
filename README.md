# kmi-scraper

Made because the wu API is down and the accuweather API has a 50 calls/day limit.
Respect https://www.meteo.be/meteo/view/en/65691-Disclaimer.html

## Usage

`python kmi-scraper.py <url>`

e.g. `python kmi-scraper.py https://www.meteo.be/meteo/view/nl/123386-Waarnemingen.html`

## Ouput

```javascript
{
	"Bierset": {
		"cityCode": 6478,
		"t": 1.8,
		"rh": 82,
		"p": 1014.8,
		"wcdn": "ZZW",
		"wcdf": 3.927,
		"wvkh": 22.0,
		"wvkn": 11.879,
		"desc": "zwaarbewolkt",
		"estc": 0.75,
		"estr": 0,
		"ests": 0
	}
}
```
- cityCode: idk
- t: temp, °celcius
- rh: relative humidity, %
- p: atmospheric pressure, Pa
- cdn: wind cardinal direction name
- cdf: cd float, 0 - TAU
- wvkh: wind velocity, km/h
- wvkn: wind velocity, knots
- desc: description
- estc: estimated cloudcover (bad, based on description), 0 - 1
- estr: estimated rain, 0 - 1
- ests: estimated snow, 0 - 1