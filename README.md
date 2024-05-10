# Harrogate Bin Day for Home Assistant

## Installation
* Normal HACS installation
* Add integration
* Add your property UPRN
  * Can find it [here](https://secure.harrogate.gov.uk/inmyarea/Search/Results/?q=&lat=0.0&lon=0.0)  after searching (https://secure.harrogate.gov.uk/inmyarea/Property/?uprn=XXXXXXXXX) 

## Usage
It will create an entity with the state being the date, and some attributes:
* `type`: `Recycling`, `Garden`, `Refuse`
* `hours_until`: How many hours until collection time (set it to 7am)
* `note`: `null` or `str`, could be anything, but usually a note saying why a collection is delayed
* `taken_out`: `boolean` stating if the bin is taken out (see [Services](#services)). 
  * Will automatically be reset to `false` once the date updates 

<a name="services"></a>
## Services
This integration adds 2 services:

* `harrogate_bin.bin_taken_out`: Updates the sensors `taken_out` to be `true`
* `harrogate_bin.bin_reset_taken_out`: Updates the sensors `taken_out` to be `false`