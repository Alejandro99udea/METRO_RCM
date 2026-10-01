/**
 * METRO_RCM - Backend central de ponderacion (5 criterios)
 * Hoja central: 1TaD-4tvKPTdAO6r0mGmihyv7OTFcYYDKfZPU8lYNga8
 * Hoja de datos: Ponderacion
 */
const SPREADSHEET_ID = '1TaD-4tvKPTdAO6r0mGmihyv7OTFcYYDKfZPU8lYNga8';
const SHEET_NAME = 'Ponderacion';
const HEADERS = ['Fecha/Hora','Evaluador','Seguridad','Impacto a la operacion','Continuidad operacional','Costo de reparacion','Impacto ambiental'];

const SEMILLA = [
  ['Datos iniciales - historico','Sebastian Osorio Medina',40,15,25,5,15],
  ['Datos iniciales - historico','Hernan Inchima',40,25,20,5,10],
  ['Datos iniciales - historico','nikoll e',25,27,22,15,11],
  ['Datos iniciales - historico','Felix anaya',47,9,22,13,9],
  ['Datos iniciales - historico','Ivan Baron',40,15,30,10,5]
];

function getSheet_(){
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  let sh = ss.getSheetByName(SHEET_NAME);
  if(!sh) sh = ss.insertSheet(SHEET_NAME);
  if(sh.getLastRow() === 0){
    sh.getRange(1,1,1,HEADERS.length).setValues([HEADERS]);
    sh.setFrozenRows(1);
  } else {
    sh.getRange(1,1,1,HEADERS.length).setValues([HEADERS]);
  }
  return sh;
}
function publicar_hoja(){ getSheet_(); }
function sembrar_votaciones_iniciales(){
  const sh=getSheet_();
  const data=sh.getDataRange().getValues();
  const nombres=new Set(data.slice(1).map(r=>String(r[1]||'').trim().toLowerCase()));
  const pendientes=SEMILLA.filter(r=>!nombres.has(String(r[1]).trim().toLowerCase()));
  if(pendientes.length){
    const filas=pendientes.map(r=>[new Date(),r[1],r[2],r[3],r[4],r[5],r[6]]);
    sh.getRange(sh.getLastRow()+1,1,filas.length,HEADERS.length).setValues(filas);
  }
  return `Sembradas ${pendientes.length} respuestas iniciales.`;
}
function doGet(e){
  try{
    const p=e&&e.parameter?e.parameter:{}; const action=String(p.action||'list').toLowerCase(); const cb=p.callback; const sh=getSheet_();
    if(action==='add'){
      const nombre=String(p.nombre||'').trim(); const votos=JSON.parse(p.votos||'[]');
      if(!nombre) throw new Error('Falta el nombre del participante.');
      if(!Array.isArray(votos)||votos.length!==5) throw new Error('La respuesta debe contener 5 valores.');
      if(votos.reduce((a,b)=>a+Number(b||0),0)!==100) throw new Error('Los puntos deben sumar exactamente 100.');
      votos.forEach(v=>{ if(Number(v)<0||Number(v)>100) throw new Error('Valor fuera de rango.'); });
      const lock=LockService.getScriptLock(); lock.waitLock(10000); try{sh.appendRow([new Date(),nombre,...votos.map(Number)]);} finally{lock.releaseLock();}
      return jsonp_({ok:true,mensaje:'Respuesta registrada.'},cb);
    }
    if(action!=='list') return jsonp_({ok:false,error:'Accion no valida.'},cb);
    if(sh.getLastRow()<=1) sembrar_votaciones_iniciales();
    const last=sh.getLastRow(); const rows=last>1?sh.getRange(2,1,last-1,HEADERS.length).getValues():[];
    const registros=rows.map((r,i)=>({id:i+1,fecha:r[0] instanceof Date?Utilities.formatDate(r[0],Session.getScriptTimeZone(),'dd/MM/yyyy HH:mm:ss'):String(r[0]||''),nombre:String(r[1]||''),seguridad:Number(r[2]||0),operacion:Number(r[3]||0),continuidad:Number(r[4]||0),costo:Number(r[5]||0),ambiental:Number(r[6]||0)}));
    const total=registros.length; const sum=[0,0,0,0,0]; registros.forEach(r=>[r.seguridad,r.operacion,r.continuidad,r.costo,r.ambiental].forEach((v,i)=>sum[i]+=v));
    const promedios=total?sum.map(v=>v/total):[0,0,0,0,0];
    return jsonp_({ok:true,total,promedios,registros},cb);
  }catch(err){return jsonp_({ok:false,error:String(err.message||err)},e&&e.parameter?e.parameter.callback:null);}
}
function doPost(e){
  try{
    const p=e&&e.parameter?e.parameter:{}; p.action=p.action||'add'; return doGet({parameter:p});
  }catch(err){return ContentService.createTextOutput(JSON.stringify({ok:false,error:String(err.message||err)})).setMimeType(ContentService.MimeType.JSON);}
}
function jsonp_(obj,cb){const payload=JSON.stringify(obj); if(cb){const safe=String(cb).replace(/[^A-Za-z0-9_]/g,''); return ContentService.createTextOutput(`${safe}(${payload});`).setMimeType(ContentService.MimeType.JAVASCRIPT);} return ContentService.createTextOutput(payload).setMimeType(ContentService.MimeType.JSON);}
