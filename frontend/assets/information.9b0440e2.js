import{_ as B}from"./index.f83d805f.js";import{C as D,D as h,I as V,F as w,w as x}from"./element-plus.ef27c94c.js";import{_ as k}from"./picker.046ca35c.js";import{a as j,b as N}from"./website.d05f3e7d.js";import{u as L,f as U}from"./index.0fb45745.js";import{d as _,r as q,a1 as y,an as O,o as c,c as I,X as u,P as l,a as r,u as t,Q as S,O as G,U as R}from"./@vue.a137a740.js";import"./@vueuse.07613b64.js";import"./@element-plus.3660753f.js";import"./lodash-es.a31ceab4.js";import"./dayjs.4eb0747d.js";import"./axios.317db7a7.js";import"./async-validator.fb49d0f5.js";import"./@ctrl.fd318bfa.js";import"./@popperjs.36402333.js";import"./escape-html.e5dfadb9.js";import"./normalize-wheel-es.8aeb3683.js";import"./index.70072f9d.js";import"./index.a8985849.js";import"./usePaging.c15919e0.js";import"./index.0fbd35aa.js";import"./index.vue_vue_type_script_setup_true_lang.c58ce5d0.js";import"./vue3-video-play.b1eef99b.js";import"./vuedraggable.0ebeab5f.js";import"./vue.de363efb.js";import"./sortablejs.cffe02b4.js";import"./lodash.329a9ebf.js";import"./vue-router.9605b890.js";import"./pinia.9b4180ce.js";import"./css-color-function.32b8b184.js";import"./color.3683ba49.js";import"./clone.a10503d0.js";import"./color-convert.755d189f.js";import"./color-name.e7a4e1d3.js";import"./color-string.e356f5de.js";import"./balanced-match.d2a36341.js";import"./ms.564e106c.js";import"./nprogress.c50c242d.js";import"./vue-clipboard3.51d666ae.js";import"./clipboard.e9b83688.js";import"./echarts.7e912674.js";import"./zrender.754e8e90.js";import"./tslib.60310f1a.js";import"./highlight.js.7165574c.js";import"./@highlightjs.7fc78ec7.js";const W={class:"website-information"},P=r("div",{class:"text-xl font-medium mb-[20px]"},"\u540E\u53F0\u8BBE\u7F6E",-1),Q={class:"w-80"},T=r("div",{class:"form-tips"},"\u5EFA\u8BAE\u5C3A\u5BF8\uFF1A100*100\u50CF\u7D20\uFF0C\u652F\u6301jpg\uFF0Cjpeg\uFF0Cpng\u683C\u5F0F",-1),X=r("div",{class:"form-tips"},"\u5EFA\u8BAE\u5C3A\u5BF8\uFF1A200*200\u50CF\u7D20\uFF0C\u652F\u6301jpg\uFF0Cjpeg\uFF0Cpng\u683C\u5F0F",-1),z=r("div",{class:"form-tips"},"\u5EFA\u8BAE\u5C3A\u5BF8\uFF1A400*400\u50CF\u7D20\uFF0C\u652F\u6301jpg\uFF0Cjpeg\uFF0Cpng\u683C\u5F0F",-1),H=r("div",{class:"text-xl font-medium mb-[20px]"},"\u524D\u53F0\u8BBE\u7F6E",-1),J={class:"w-80"},K=r("div",{class:"form-tips"},"\u5EFA\u8BAE\u5C3A\u5BF8\uFF1A100*100px\uFF0C\u652F\u6301jpg\uFF0Cjpeg\uFF0Cpng\u683C\u5F0F",-1),M=_({name:"webInformation"}),Qo=_({...M,setup(Y){const p=q(),{getConfig:g}=L(),o=y({name:"",favicon:"",logo:"",backdrop:"",shopName:"",shopLogo:""}),f={name:[{required:!0,message:"\u8BF7\u8F93\u5165\u7F51\u7AD9\u540D\u79F0",trigger:["blur"]}],favicon:[{required:!0,message:"\u8BF7\u9009\u62E9\u7F51\u7AD9\u56FE\u6807",trigger:["change"]}],logo:[{required:!0,message:"\u8BF7\u9009\u62E9\u7F51\u7AD9logo",trigger:["change"]}],backdrop:[{required:!0,message:"\u8BF7\u9009\u62E9\u767B\u5F55\u9875\u5E7F\u544A\u56FE",trigger:["change"]}],shopName:[{required:!0,message:"\u8BF7\u8F93\u5165\u5E97\u94FA/\u5546\u57CE\u540D\u79F0",trigger:["blur"]}],shopLogo:[{required:!0,message:"\u8BF7\u9009\u62E9\u5546\u57CELOGO",trigger:["change"]}]},n=async()=>{const i=await j();for(const e in o)o[e]=i[e]},C=async()=>{var i;await((i=p.value)==null?void 0:i.validate()),await N(o),U.msgSuccess("\u64CD\u4F5C\u6210\u529F"),g(),n()};return n(),(i,e)=>{const F=D,s=h,m=k,d=V,E=w,b=x,v=B,A=O("perms");return c(),I("div",W,[u(E,{ref_key:"formRef",ref:p,rules:f,model:t(o),"label-width":"120px"},{default:l(()=>[u(d,{shadow:"never",class:"!border-none"},{default:l(()=>[P,u(s,{label:"\u7F51\u7AD9\u540D\u79F0",prop:"name"},{default:l(()=>[r("div",Q,[u(F,{modelValue:t(o).name,"onUpdate:modelValue":e[0]||(e[0]=a=>t(o).name=a),placeholder:"\u8BF7\u8F93\u5165\u7F51\u7AD9\u540D\u79F0",maxlength:"30","show-word-limit":""},null,8,["modelValue"])])]),_:1}),u(s,{label:"\u7F51\u7AD9\u56FE\u6807",prop:"favicon"},{default:l(()=>[r("div",null,[u(m,{modelValue:t(o).favicon,"onUpdate:modelValue":e[1]||(e[1]=a=>t(o).favicon=a),limit:1},null,8,["modelValue"]),T])]),_:1}),u(s,{label:"\u7F51\u7AD9logo",prop:"logo"},{default:l(()=>[r("div",null,[u(m,{modelValue:t(o).logo,"onUpdate:modelValue":e[2]||(e[2]=a=>t(o).logo=a),limit:1},null,8,["modelValue"]),X])]),_:1}),u(s,{label:"\u767B\u5F55\u9875\u5E7F\u544A\u56FE",prop:"backdrop"},{default:l(()=>[r("div",null,[u(m,{modelValue:t(o).backdrop,"onUpdate:modelValue":e[3]||(e[3]=a=>t(o).backdrop=a),limit:1},null,8,["modelValue"]),z])]),_:1})]),_:1}),u(d,{shadow:"never",class:"!border-none mt-4"},{default:l(()=>[H,u(s,{label:"\u5546\u57CE\u540D\u79F0",prop:"shopName"},{default:l(()=>[r("div",J,[u(F,{modelValue:t(o).shopName,"onUpdate:modelValue":e[4]||(e[4]=a=>t(o).shopName=a),placeholder:"\u8BF7\u8F93\u5165\u5E97\u94FA/\u5546\u57CE\u540D\u79F0",maxlength:"30","show-word-limit":""},null,8,["modelValue"])])]),_:1}),u(s,{label:"\u5546\u57CELOGO",prop:"shopLogo"},{default:l(()=>[r("div",null,[u(m,{modelValue:t(o).shopLogo,"onUpdate:modelValue":e[5]||(e[5]=a=>t(o).shopLogo=a),limit:1},null,8,["modelValue"]),K])]),_:1})]),_:1})]),_:1},8,["model"]),S((c(),G(v,null,{default:l(()=>[u(b,{type:"primary",onClick:C},{default:l(()=>[R("\u4FDD\u5B58")]),_:1})]),_:1})),[[A,["setting:website:save"]]])])}}});export{Qo as default};