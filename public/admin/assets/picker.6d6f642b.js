import{P as I}from"./index.7735a16f.js";import{E as T}from"./element-plus.f12e93f2.js";import{F as N,_ as E,a as M}from"./index.c78ec804.js";import{u as K,d as Q,b as X}from"./index.e3e224d5.js";import{_ as Y}from"./index.81942e9e.js";import{D as j}from"./vuedraggable.8ce16c30.js";import{f as q}from"./@vueuse.07613b64.js";import{d as G,r as i,ab as H,e as S,w as J,E as P,n as O,ag as U,o as W,c as Z,X as n,aa as x,P as p,a as s,$ as V,R as k,U as ee,Q as le,K as ae,a0 as te,Y as oe,b7 as se,b6 as ie}from"./@vue.a137a740.js";const ne=G({components:{Popup:I,Draggable:j,FileItem:N,Material:E,Preview:M},props:{modelValue:{type:[String,Array],default:()=>[]},type:{type:String,default:"image"},size:{type:String,default:"100px"},fileSize:{type:String,default:"100px"},limit:{type:Number,default:1},disabled:{type:Boolean,default:!1},hiddenUpload:{type:Boolean,default:!1},uploadClass:{type:String,default:""},excludeDomain:{type:Boolean,default:!1}},emits:["change","update:modelValue"],setup(e,{emit:t}){const h=i(),g=i(),_=i(""),w=i(!1),a=i([]),m=i([]),r=i(!0),c=i(-1),{disabled:y,limit:u,modelValue:C}=H(e),{getImageUrl:b}=K(),o=S(()=>{switch(e.type){case"image":return"\u56FE\u7247";case"video":return"\u89C6\u9891";default:return""}}),f=S(()=>e.limit-a.value.length>0),v=S(()=>r.value?u.value==-1?null:u.value-a.value.length:1),D=q(()=>{const l=m.value.map(d=>e.excludeDomain?d.path:d.uri);r.value?a.value=[...a.value,...l]:a.value.splice(c.value,1,l.shift()),$()},1e3,!1),A=l=>{var d;y.value||(l>=0?(r.value=!1,c.value=l):r.value=!0,(d=h.value)==null||d.open())},F=l=>{m.value=l},$=()=>{const l=u.value!=1?a.value:a.value[0]||"";t("update:modelValue",l),t("change",l),z()},R=l=>{a.value.splice(l,1),$()},L=l=>{_.value=l,w.value=!0},z=()=>{O(()=>{var l;e.hiddenUpload&&(a.value=[]),(l=g.value)==null||l.clearSelect()})};return J(C,l=>{a.value=Array.isArray(l)?l:l==""?[]:[l]},{immediate:!0}),P("limit",e.limit),P("hiddenUpload",e.hiddenUpload),{popupRef:h,materialRef:g,fileList:a,tipsText:o,handleConfirm:D,meterialLimit:v,showUpload:f,showPopup:A,selectChange:F,deleteImg:R,previewUrl:_,showPreview:w,handlePreview:L,handleClose:z,getImageUrl:b}}});const B=e=>(se("data-v-d1489be1"),e=e(),ie(),e),re={class:"material-select"},ue=["onClick"],de={class:"operation-btns text-xs text-center"},pe=B(()=>s("span",null,"\u4FEE\u6539",-1)),me=["onClick"],ce=B(()=>s("span",null,"\u6DFB\u52A0",-1)),fe={class:"material-wrap"};function ve(e,t,h,g,_,w){const a=U("file-item"),m=Y,r=U("draggable"),c=X,y=E,u=T,C=I,b=U("preview");return W(),Z("div",re,[n(C,{ref:"popupRef",width:"830px","custom-class":"body-padding",title:`\u9009\u62E9${e.tipsText}`,onConfirm:e.handleConfirm,onClose:e.handleClose},x({default:p(()=>[n(u,null,{default:p(()=>[s("div",fe,[n(y,{ref:"materialRef",type:e.type,"file-size":e.fileSize,limit:e.meterialLimit,onChange:e.selectChange},null,8,["type","file-size","limit","onChange"])])]),_:1})]),_:2},[e.hiddenUpload?void 0:{name:"trigger",fn:p(()=>[s("div",{class:"material-select__trigger clearfix",onClick:t[2]||(t[2]=V(()=>{},["stop"]))},[n(r,{class:"draggable",modelValue:e.fileList,"onUpdate:modelValue":t[0]||(t[0]=o=>e.fileList=o),animation:"300","item-key":"id"},{item:p(({element:o,index:f})=>[s("div",{class:k(["material-preview",{"is-disabled":e.disabled,"is-one":e.limit==1}]),onClick:v=>e.showPopup(f)},[n(m,{onClose:v=>e.deleteImg(f)},{default:p(()=>[n(a,{uri:e.excludeDomain?e.getImageUrl(o):o,"file-size":e.size,type:e.type},null,8,["uri","file-size","type"])]),_:2},1032,["onClose"]),s("div",de,[pe,ee(" | "),s("span",{onClick:V(v=>e.handlePreview(o),["stop"])},"\u67E5\u770B",8,me)])],10,ue)]),_:1},8,["modelValue"]),le(s("div",{class:k(["material-upload",{"is-disabled":e.disabled,"is-one":e.limit==1,[e.uploadClass]:!0}]),onClick:t[1]||(t[1]=o=>e.showPopup(-1))},[ae(e.$slots,"upload",{},()=>[s("div",{class:"upload-btn",style:te({width:e.size,height:e.size})},[n(c,{size:25,name:"el-icon-Plus"}),ce],4)],!0)],2),[[oe,e.showUpload]])])]),key:"0"}]),1032,["title","onConfirm","onClose"]),n(b,{modelValue:e.showPreview,"onUpdate:modelValue":t[3]||(t[3]=o=>e.showPreview=o),url:e.previewUrl,type:e.type},null,8,["modelValue","url","type"])])}const Ue=Q(ne,[["render",ve],["__scopeId","data-v-d1489be1"]]);export{Ue as _};
