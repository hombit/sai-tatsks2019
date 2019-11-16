/*! */
riot.tag2("multimodel",'<div class="mobile-header"><div class="mh-closing-x iconfont clickable" data-do="rqstClose,multimodel">}</div> {t.ND_COMPARE} </div><div class="plugin-content detail" ref="content"><div class="loading full {show: loader}"></div><div if="{! loader}" each="{model in modelsLoaded}" class="model-box" data-model="{model}" no-reorder><div class="legend"></div><div class="forecast-table"><canvas></canvas><table class="noselect"></table><b></b></div><div class="multi-model-desc"><a data-do="url,{models[ model ].url}"><img riot-src="https://www.windy.com/img/providers/{models[ model ].provider}-grey.svg"></a> {modelsDesc[ model ]} <br><br> {t.MENU_D_UPDATED}: {models[ model ].header && models[ model ].header.update}<br> {t.MENU_D_REFTIME}: {models[ model ].header && models[ model ].header.refTime} </div><div class="model-title height-days">{models[ model ].name}</div></div></div>',".onmultimodel #rhpane{display:none}#device-mobile .onmultimodel #user,#device-mobile .onmultimodel #search{display:none !important}#plugin-multimodel{position:fixed;left:0;right:0;max-height:calc(100vh - 80px);bottom:0;z-index:20;transition:transform .15s ease-in-out;-webkit-transition:transform .15s ease-in-out;transform:translate(0, 110%);-webkit-transform:translate(0, 110%)}#plugin-multimodel.open{transform:none;-webkit-transform:none}#plugin-multimodel .closing-x{display:block;font-size:40px;top:-0.7em;left:.1em;right:initial}#plugin-multimodel .plugin-content{cursor:-webkit-grab;cursor:-moz-grab;cursor:grab;padding:10px 15px 10px 15px;font-size:14px;overflow-x:auto;overflow-y:auto;position:relative;max-height:calc(100vh - 80px);min-height:200px}#plugin-multimodel .plugin-content::-webkit-scrollbar{width:10px;height:8px}#plugin-multimodel .detail .legend .legend-rain{padding-top:0}#plugin-multimodel .detail .height-rain{height:16px}#plugin-multimodel .detail .forecast-table canvas{top:28px}#device-mobile #plugin-multimodel{max-height:initial}#device-mobile #plugin-multimodel .closing-x{top:0;right:inherit;bottom:inherit;width:1em}#device-mobile #plugin-multimodel .plugin-content{position:absolute;overflow-y:scroll;max-height:100vh}#plugin-multimodel .model-box{font-size:12px;position:relative;clear:both;white-space:nowrap;display:flex}#plugin-multimodel .model-box .forecast-table{position:relative}#plugin-multimodel .model-box .forecast-table b{top:30px}#plugin-multimodel .model-box .model-title{position:absolute;left:0;top:9px;z-index:10;color:#444;width:95px;height:28px}#plugin-multimodel .model-box .sticky-title{font-size:11px;color:#777}#plugin-multimodel .model-box .legend{padding-bottom:1px}#plugin-multimodel .model-box .height-icon{height:25px}#plugin-multimodel .model-box .height-temp{height:20px}#plugin-multimodel .model-box .td-icon img{width:20px;height:20px}#plugin-multimodel .model-box .multi-model-desc{min-width:300px;white-space:normal;font-size:10px;padding:28px 15px 0 10px}#plugin-multimodel .model-box .multi-model-desc img{width:100px;max-height:50px;position:relative;float:right;margin-top:-10px}","",function(e){var o=this,t=W.require,i=t("store"),l=t("query"),n=t("reverseName"),d=t("trans"),a=t("$"),m=t("multiLoad"),r=t("picker"),s=t("models"),p=t("DraggableDiv"),u=t("weatherRenderExtended"),c={},h=!1,g=!1;this.t=d,this.models={ecmwf:{name:"ECMWF 9km",provider:"ecmwf",url:"https://www.ecmwf.int/"},gfs:{name:"GFS 22km",provider:"noaa",url:"https://www.noaa.gov/"},mblue:{name:"METEOBLUE",provider:"meteoblue",url:"https://www.meteoblue.com/"},namConus:{name:"NAM 5km",provider:"noaa",url:"https://www.noaa.gov/"},namAlaska:{name:"NAM 5km",provider:"noaa",url:"https://www.noaa.gov/"},namHawaii:{name:"NAM 2km",provider:"noaa",url:"https://www.noaa.gov/"},iconEu:{name:"ICON-EU 6km",provider:"dwd",url:"https://www.dwd.de/"},arome:{name:"AROME 1.3km",provider:"fr",url:"http://www.meteofrance.com/"}},this.modelsDesc={ecmwf:"Very accurate model provided by European Centre for Medium-Range Weather Forecasts.\n\t\t\t\tClear winner compared to other forecast models. Since the model is commercial, only few companies in the World offer it.",gfs:"Basic free model provided by National Oceanic and Atmospheric Administration with not so good resolution.\n\t\t\t\tCompared to other models GFS can fail in mountain areas, and by forecasting clouds and precipitation.\n\t\t\t\tSince the model is free, majority of weather applications use GFS.",mblue:"Ensemble of multiple global and local forecast models using AI. Developed by Swiss company Meteoblue beats other models in temperatures\n\t\t\t\tand wind. Excells especially in Alpine areas.",iconEu:"High resolution model developed and operated by German DWD. One of the most modern forecast models delivering very good results in Europe.",namConus:"Regional mesoscale model run by NCEP. Provides better resolution than global models.",namHawaii:"Regional mesoscale model run by NCEP. Provides better resolution than global models.",namAlaska:"Regional mesoscale model run by NCEP. Provides better resolution than global models.",arome:"High resolution model developed and operated by Meteo France."},this.modelsUse={ecmwf:"Windy.com, Yr.no",gfs:"Windguru, Windfinder",mblue:"Meteoblue",iconEu:"Ventusky"},this.modelsLoaded=[];var f={rows:["hour","icon","temp","wind","windDir","rain"],tdWidth:32,iconSize:25,days:5,step:3,display:"table",params:c};this.on("mount",function(){return p.instance({scrollEl:o.refs.content})}),this.onopen=function(e){var t=i.get("detailLocation");c=e||t,g=!!t,o.modelsLoaded=[],o.update({loader:!0});var d=s.getPointProducts(c);m(c,d).then(function(e){o.modelsLoaded=e.map(function(e){return e.model}),o.loader=!1,o.update(),v(e)}).catch(window.wError.bind(null,"multimodel","Loading/rendering models")),g||n.get(c).then(function(e){return l.set(e.name)}),h||(r.on("pickerOpened",o.onopen),r.on("pickerMoved",o.onopen),h=!0)},this.onclose=function(){g||l.set(""),h&&(r.off("pickerOpened",o.onopen),r.off("pickerMoved",o.onopen))},this.onurl=function(){return{url:"multimodel/"+c.lat+"/"+c.lon,title:"Compare GFS, ECMWF, NEMS"}};var b=function(e){var t=e.fcst,i=e.model;if(t){var l=a('[data-model="'+i+'"]',o.root);u.init(l,t,f).renderTable().renderBackground({tempH:70}),o.models[i].header=t.header,o.update()}},v=function(e){e.forEach(b),d.translateDocument(o.root),w()},w=function(){var e=o.refs.content,t=a("#plugin-multimodel");document.body.offsetHeight-e.offsetHeight<95?t.classList.add("mm-fullscreen"):t.classList.remove("mm-fullscreen")}});