export const CD: Record<string, any> = {
  '6m':{ labels:['Jul 24','Aug 24','Sep 24','Oct 24','Nov 24','Dec 24','Jan 25','Feb 25','Mar 25','Apr 25','May 25','Jun 25'],
    aqua:[6800,6950,7100,7050,7300,7420,7350,7500,7420,7550,7600,7680],vezel:[9200,9400,9500,9350,9600,9750,9700,9800,9900,9850,10100,10200],
    alto:[3800,3900,3850,3950,4100,4050,4200,4150,4300,4250,4400,4350],leaf:[5200,5400,5300,5500,5600,5700,5650,5800,5750,5900,5950,6100],
    prius:[8200,8350,8400,8300,8500,8700,8650,8800,8900,8850,9000,9100]},
  '1y':{ labels:['Jan 24','Feb 24','Mar 24','Apr 24','May 24','Jun 24','Jul 24','Aug 24','Sep 24','Oct 24','Nov 24','Dec 24','Jan 25','Feb 25','Mar 25','Apr 25','May 25','Jun 25'],
    aqua:[6200,6350,6400,6500,6600,6700,6800,6950,7100,7050,7300,7420,7350,7500,7420,7550,7600,7680],
    vezel:[8500,8700,8800,8900,9000,9100,9200,9400,9500,9350,9600,9750,9700,9800,9900,9850,10100,10200],
    alto:[3400,3500,3550,3600,3650,3700,3800,3900,3850,3950,4100,4050,4200,4150,4300,4250,4400,4350],
    leaf:[4600,4800,4900,5000,5100,5200,5200,5400,5300,5500,5600,5700,5650,5800,5750,5900,5950,6100],
    prius:[7600,7700,7800,7900,8000,8100,8200,8350,8400,8300,8500,8700,8650,8800,8900,8850,9000,9100]},
  'all':{ labels:['2022 Q1','Q2','Q3','Q4','2023 Q1','Q2','Q3','Q4','2024 Q1','Q2','Q3','Q4'],
    aqua:[5800,6000,6200,6400,6600,6900,7100,7300,7420,7550,7650,7680],vezel:[7800,8100,8400,8700,9000,9300,9500,9700,9900,10050,10150,10200],
    alto:[3000,3100,3200,3400,3550,3700,3850,4000,4100,4250,4350,4350],leaf:[3800,4100,4400,4700,5000,5200,5400,5600,5750,5900,6000,6100],
    prius:[7000,7200,7400,7600,7800,8000,8200,8400,8600,8750,8900,9100]}
};

export const MODELS_BY_MAKE: Record<string, string[]> = {
  Toyota:['Aqua','Prius','Axio','Allion','Vitz','RAV4','Land Cruiser','Hilux'],
  Honda:['Vezel','Fit','City','Civic','CR-V','Jazz'],
  Suzuki:['Alto','Swift','Wagon R','Jimny','Every','Spacia'],
  Nissan:['Leaf','Sunny','Tiida','X-Trail','March','Note'],
  Mitsubishi:['Lancer','Outlander','ASX','Attrage'],
  BMW:['X1','X3','X5','3 Series','5 Series'],
  Mercedes:['C200','E200','GLC','A-Class','S-Class'],
  Mazda:['Demio','Axela','CX-5','CX-3'],
  Perodua:['Axia','Myvi','Alza','Bezza']
};

export const MARKET_AVG: Record<string, number> = {
  'Toyota_Aqua':7420,'Toyota_Prius':8900,'Toyota_Axio':6800,'Toyota_Allion':7200,'Toyota_Vitz':5100,'Toyota_RAV4':14200,
  'Honda_Vezel':10200,'Honda_Fit':5200,'Honda_City':7800,'Honda_Civic':9500,'Honda_CR-V':13500,'Honda_Jazz':5600,
  'Suzuki_Alto':4350,'Suzuki_Swift':5800,'Suzuki_Wagon R':5100,'Suzuki_Jimny':9800,
  'Nissan_Leaf':6100,'Nissan_Sunny':4200,'Nissan_X-Trail':11500,'Nissan_Tiida':4600,
  'Mitsubishi_Lancer':6450,'Mitsubishi_Outlander':12800,'Mitsubishi_ASX':9200,
  'BMW_X1':18500,'BMW_X3':24000,'BMW_3 Series':16800,'BMW_5 Series':22000,
  'Mercedes_C200':22000,'Mercedes_E200':28000,'Mercedes_GLC':32000,
  'Mazda_Demio':5750,'Mazda_Axela':7200,'Mazda_CX-5':14800,
  'Perodua_Axia':3900,'Perodua_Myvi':5200,'Perodua_Alza':6800
};

export const HISTORY: Record<string, number[]> = {
  'Toyota_Aqua':[6200,6350,6500,6700,6900,7100,7050,7300,7420,7350,7500,7680],
  'Honda_Vezel':[8500,8700,8900,9100,9400,9500,9350,9600,9750,9700,9800,10200],
  'Suzuki_Alto':[3400,3500,3600,3700,3800,3850,3950,4050,4100,4200,4300,4350],
  'Nissan_Leaf':[4600,4800,5000,5200,5400,5300,5500,5600,5700,5650,5800,6100],
  'Toyota_Prius':[7600,7800,8000,8100,8350,8400,8300,8500,8700,8650,8800,9100],
  'Honda_Fit':[4400,4500,4600,4700,4800,4900,4950,5000,5050,5100,5150,5200],
  'Mitsubishi_Lancer':[5800,5900,6000,6100,6200,6300,6250,6300,6350,6400,6420,6450],
  'Mazda_Demio':[5100,5200,5300,5400,5500,5600,5600,5680,5720,5750,5750,5750],
  'Perodua_Axia':[3200,3300,3400,3500,3600,3700,3750,3800,3820,3850,3880,3900]
};

export const BRANDS = [
  {name:'Toyota',  logo:'🚗',cat:'japanese',models:68,change:'+2.4%',up:true, avgPrice:'Rs. 8.2M', count:3420,goodRate:'14%',hist:[7800,8000,8100,8050,8200,8200]},
  {name:'Honda',   logo:'🚙',cat:'japanese',models:26,change:'+1.8%',up:true, avgPrice:'Rs. 7.4M', count:1980,goodRate:'11%',hist:[7000,7100,7200,7150,7300,7400]},
  {name:'BMW',     logo:'🏎', cat:'european',models:50,change:'+0.6%',up:true, avgPrice:'Rs. 19.8M',count:480, goodRate:'8%', hist:[19000,19200,19500,19400,19700,19800]},
  {name:'Mercedes',logo:'⭐',cat:'european',models:47,change:'-0.3%',up:false,avgPrice:'Rs. 24.1M',count:310, goodRate:'6%', hist:[24500,24300,24100,24200,24000,24100]},
  {name:'Nissan',  logo:'🔵',cat:'japanese',models:35,change:'+3.4%',up:true, avgPrice:'Rs. 6.1M', count:1540,goodRate:'13%',hist:[5600,5700,5800,5900,6000,6100]},
  {name:'Suzuki',  logo:'🟡',cat:'japanese',models:28,change:'-0.5%',up:false,avgPrice:'Rs. 4.8M', count:2100,goodRate:'16%',hist:[4900,4850,4800,4820,4800,4800]},
  {name:'Audi',    logo:'🔶',cat:'european',models:13,change:'+1.1%',up:true, avgPrice:'Rs. 16.4M',count:220, goodRate:'7%', hist:[16000,16100,16200,16300,16400,16400]},
  {name:'Land Rover',logo:'🌿',cat:'european',models:9,change:'+2.0%',up:true, avgPrice:'Rs. 28.5M',count:140, goodRate:'5%', hist:[27500,27800,28000,28200,28400,28500]},
  {name:'Mitsubishi',logo:'🔷',cat:'japanese',models:23,change:'+1.4%',up:true, avgPrice:'Rs. 9.2M', count:870, goodRate:'12%',hist:[8800,8900,9000,9100,9100,9200]},
  {name:'Kia',     logo:'🟠',cat:'korean',  models:17,change:'+2.8%',up:true, avgPrice:'Rs. 8.9M', count:640, goodRate:'10%',hist:[8400,8500,8600,8700,8800,8900]},
  {name:'Daihatsu',logo:'⬛',cat:'japanese',models:17,change:'-1.2%',up:false,avgPrice:'Rs. 3.6M', count:720, goodRate:'18%',hist:[3700,3700,3650,3620,3600,3600]},
  {name:'Mazda',   logo:'🔴',cat:'japanese',models:14,change:'+1.6%',up:true, avgPrice:'Rs. 6.8M', count:590, goodRate:'11%',hist:[6400,6500,6600,6650,6700,6800]},
  {name:'Hyundai', logo:'🔘',cat:'korean',  models:12,change:'+1.9%',up:true, avgPrice:'Rs. 7.6M', count:480, goodRate:'10%',hist:[7200,7300,7400,7450,7500,7600]},
  {name:'Perodua', logo:'🟢',cat:'other',   models:8, change:'+2.1%',up:true, avgPrice:'Rs. 4.8M', count:820, goodRate:'15%',hist:[4400,4500,4600,4650,4700,4800]},
  {name:'Isuzu',   logo:'🚛',cat:'japanese',models:6, change:'+0.9%',up:true, avgPrice:'Rs. 11.2M',count:280, goodRate:'9%', hist:[10800,10900,11000,11100,11100,11200]},
  {name:'Volvo',   logo:'🔷',cat:'european',models:8, change:'-0.4%',up:false,avgPrice:'Rs. 22.8M',count:90,  goodRate:'6%', hist:[23000,22900,22900,22800,22800,22800]},
  {name:'Jeep',    logo:'🟤',cat:'other',   models:7, change:'+1.2%',up:true, avgPrice:'Rs. 17.4M',count:110, goodRate:'7%', hist:[17000,17100,17200,17300,17400,17400]},
  {name:'44 more', logo:'➕',cat:'other',   models:0, change:'',      up:true, avgPrice:'—',        count:0,   goodRate:'—',  hist:[]}
];

export const DISTRICTS = [
  {name:'Colombo',price:'Rs. 9.1M',count:6240},{name:'Gampaha',price:'Rs. 8.4M',count:3180},
  {name:'Kandy',price:'Rs. 7.8M',count:2410},{name:'Galle',price:'Rs. 7.2M',count:1820},
  {name:'Matara',price:'Rs. 6.9M',count:1240},{name:'Kurunegala',price:'Rs. 7.1M',count:1560},
  {name:'Ratnapura',price:'Rs. 6.8M',count:980},{name:'Kalutara',price:'Rs. 8.0M',count:1340},
  {name:'Badulla',price:'Rs. 6.5M',count:720},{name:'Anuradhapura',price:'Rs. 6.2M',count:840},
  {name:'Trincomalee',price:'Rs. 6.0M',count:580},{name:'Jaffna',price:'Rs. 6.4M',count:640},
  {name:'Batticaloa',price:'Rs. 5.8M',count:420},{name:'Polonnaruwa',price:'Rs. 5.9M',count:360},
  {name:'Matale',price:'Rs. 6.6M',count:490}
];

export const TICKERS = [
  {make:'Toyota Aqua 2016',price:'Rs. 7,680,000',delta:'+2.1%',up:true},
  {make:'Honda Vezel 2015',price:'Rs. 10,200,000',delta:'+1.8%',up:true},
  {make:'Suzuki Alto 2020',price:'Rs. 4,350,000',delta:'-0.5%',up:false},
  {make:'Nissan Leaf 2017',price:'Rs. 6,100,000',delta:'+3.4%',up:true},
  {make:'Toyota Prius 2014',price:'Rs. 8,900,000',delta:'+0.9%',up:true},
  {make:'Honda Fit 2013',price:'Rs. 5,200,000',delta:'-1.2%',up:false},
  {make:'Mazda Demio 2015',price:'Rs. 5,750,000',delta:'+1.5%',up:true},
  {make:'BMW X1 2018',price:'Rs. 18,500,000',delta:'+0.8%',up:true},
  {make:'Perodua Axia 2019',price:'Rs. 3,900,000',delta:'+2.6%',up:true},
  {make:'Mitsubishi Lancer 2014',price:'Rs. 6,450,000',delta:'+1.1%',up:true},
  {make:'Audi A3 2017',price:'Rs. 14,200,000',delta:'-0.3%',up:false},
  {make:'Suzuki Wagon R 2019',price:'Rs. 5,100,000',delta:'+1.8%',up:true}
];
