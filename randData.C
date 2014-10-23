
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=//
// Trying to generate some random data to see where   //
// events clustrering from 0-5 degree zenith will lie //
// on the galactic plane.                             //
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=//

#include "TRandom3.h"

//-----------------------------------------//
// Main
//-----------------------------------------//
void randData()
{

  // Necessary Library for coord transformation
  gSystem->Load("libcoordinate-service.so");
  using namespace std;
  using namespace SLACoordinateTransform;
  
  // Specify the number of events to generate
  int NEvents = 10000;
  
  // Make random obj
  TRandom3* r_zen  = new TRandom3(1234567);
  TRandom3* r_sign = new TRandom3(192837465);
  TRandom3* r_azi  = new TRandom3(7654321);

  // Objects for random times
  TRandom3* r_month = new TRandom3(2468753);
  TRandom3* r_day   = new TRandom3(3578642);
  TRandom3* r_hour  = new TRandom3(21436587);
  TRandom3* r_min   = new TRandom3(78563412);
  TRandom3* r_sec   = new TRandom3(90875643);

  // Specify the range for vars
  //double zen_max = TMath::Pi();
  double zen_max = TMath::Pi() * 5/180.; // Restricting to 5 degreesless
  double azi_max = 2*TMath::Pi();
  int month_max = 13;
  int day_max   = 21;
  int hour_max  = 24;
  int min_max   = 60;
  int sec_max   = 60;

  // Fix the year
  int year = 2014;
  LocalToEqua func("IceCube",year);

  // Define the variables
  double zen = 0;
  double azi = 0;
  int month = 0;
  int day   = 0;
  int hour  = 0;
  int min   = 0;
  double sec = 0;
  double lat = 0;
  double lon = 0;
  double ra  = 0;
  double dec = 0;
  
  // Make a tree
  TTree* tree = new TTree("tree","Randomly Generated Data");
  tree->Branch("zen",&zen,"zen/D");
  tree->Branch("azi",&azi,"azi/D");
  tree->Branch("month",&month,"month/I");
  tree->Branch("day",&day,"day/I");
  tree->Branch("hour",&hour,"hour/I");
  tree->Branch("min",&min,"min/I");
  tree->Branch("sec",&sec,"sec/D");
  tree->Branch("lat",&lat,"lat/D");
  tree->Branch("lon",&lon,"lon/D");
  tree->Branch("ra",&ra,"ra/D");
  tree->Branch("dec",&dec,"dec/D");

  // Loop and generate data
  for(int i=0; i<NEvents; ++i){

    // Get sign for zenith
    //int sign = (r_sign->Rndm() > 0.5 ? 1 : -1);

    // Get directions
    zen = r_zen->Rndm() * zen_max; // * sign;
    azi = r_azi->Rndm() * azi_max;
    
    // Build date
    month = (int) (r_month->Rndm() * month_max);
    day   = (int) (r_day->Rndm() * day_max);
    hour  = (int) (r_hour->Rndm() * hour_max);
    min   = (int) (r_min->Rndm() * min_max);
    sec   = r_sec->Rndm() * sec_max;

    // Catch errors
    while( month == 0 ) 
      month = (int) (r_month->Rndm() * month_max);
    while(day == 0)
      day   = (int) (r_day->Rndm() * day_max);

    // Get time in JD
    //cout<<month<<" "<<day<<" "<<hour<<" "<<min<<" "<<sec<<endl;
    double time_jd = CalendarDate2MJD(year,month,day,hour,min,sec);

    // Set detector up and load galactic and equitorial coords
    func.set_with_detector_coordinates(zen,azi,time_jd);
    func.get_galactical_coordinates(lat,lon);
    //double lat_ = 0, lon_ = 0;
    //func.get_galactical_coordinates(lat_,lon_);
    func.get_equatorial_coordinates(ra,dec);
    tree->Fill();
  }

  // Open file
  TFile* output = new TFile("test.root","recreate");
  tree->Write();
  output->Write();
  output->Close();

}
