(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[0],{222:function(e,t,a){e.exports=a.p+"static/media/operator.23ba0e19.png"},224:function(e,t,a){e.exports=a.p+"static/media/sample_input.e5d0b92e.JPG"},225:function(e,t,a){e.exports=a.p+"static/media/sample_result.3096486d.JPG"},226:function(e,t,a){e.exports=a.p+"static/media/sample_similarity.fa304a2f.JPG"},243:function(e,t,a){e.exports=a(416)},248:function(e,t,a){},266:function(e,t,a){},267:function(e,t,a){},416:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),l=a(34),o=a.n(l),i=(a(248),a(35)),s=a(36),c=a(38),u=a(37),h=a(98),m=a.n(h),d=(a(265),a(266),a(267),a(204)),p=a(39),y=a(27),g=a(442),E=a(445),f=a(68),b=a(205),v="One-Liner\nShort\nMedium\nLong".split("\n"),k="PG\nPG-13".split("\n"),j=[{categories:["Pick-up Line","Biology"]},{categories:["Pick-up Line","Pun"]},{search:"bar"},{sizes:["One-Liner"]},{search:"Chicken cross the road"},{maturity:"PG-13"},{categories:["Pun","Dad Jokes"],maturity:"PG-13"},{categories:["Pun","Dad Jokes"],maturity:"PG-13"},{categories:["Pun"],maturity:"PG-13"},{categories:["Pun"],maturity:"PG-13"},{search:"math",sizes:["Short"]},{categories:["Yo Mama"],maturity:"PG-13"},{categories:["Yo Mama"],maturity:"PG"},{categories:["Yo Mama"],maturity:"PG"}],w=function(e){Object(c.a)(a,e);var t=Object(u.a)(a);function a(e){var n;return Object(i.a)(this,a),(n=t.call(this,e)).handleChange=function(e,t){var a=t.name,r=t.value;n.setState(Object(d.a)({},a,r))},n.tonewURL=function(e,t,a,r,l){var o=new URLSearchParams,i=null===e||""===e,s=null===t||0===t.length,c=null===a||""===a,u=null===l||""===l,h=null===r||0===r.length;if(i&&s&&h&&u)n.setState({displayMessage:!0});else{i||o.append("search",e),s||t.forEach((function(e){o.append("categories",e)})),c||o.append("score",a),u||o.append("maturity",l),h||r.forEach((function(e){o.append("sizes",e)}));var m="?"+o.toString();n.props.history.push({pathname:"/",search:m})}},n.handleAdvanced=function(e,t){var a=!n.state.isOpen;n.setState({isOpen:a})},n.createDropDownList=function(e){return e.map((function(e){return{key:e,text:e,value:e}}))},n.state={isLoaded:!1,cat_options:[],categories:[],search:"",score:"",sizes:[],maturity:"",displayMessage:!1,isOpen:!1},n.advanced=r.a.createRef(),n.handleSubmit=n.handleSubmit.bind(Object(p.a)(n)),n.handleAdvanced=n.handleAdvanced.bind(Object(p.a)(n)),n.handleLucky=n.handleLucky.bind(Object(p.a)(n)),n}return Object(s.a)(a,[{key:"isOpen",value:function(){var e=this.props,t=e.categories,a=e.score,n=e.sizes,r=e.maturity,l=null===t||0===t.length,o=null===a||""===a,i=null===r||""===r,s=null===n||0===n.length,c=!l||!o||!i||!s;this.setState({isOpen:c})}},{key:"componentDidMount",value:function(){var e=this,t=this.props,a=t.categories,n=t.score,r=t.sizes,l=t.maturity,o=t.search;m()({method:"GET",url:"/api/cat-options"}).then((function(t){e.setState({cat_options:t.data.categories,isLoaded:!0,categories:a||[],score:n||"",sizes:r||[],maturity:l||"",search:o||""})})).catch((function(e){return console.log(e)})),this.isOpen()}},{key:"handleSubmit",value:function(e){e.preventDefault();var t=this.state,a=t.search,n=t.categories,r=t.score,l=t.sizes,o=t.maturity;this.tonewURL(a,n,r,l,o)}},{key:"focus",value:function(){this.advanced&&this.advanced.current.scrollIntoView({behavior:"smooth",block:"start"})}},{key:"handleLucky",value:function(e){e.preventDefault();var t=this.state.cat_options.map((function(e){return{categories:[e]}})),a=j.concat(t),n=a[Math.floor(Math.random()*a.length)],r=n.categories||[],l=n.search||"",o=n.sizes||[],i=n.maturity||"";this.tonewURL(l,r,.25,o,i)}},{key:"componentDidUpdate",value:function(){this.focus()}},{key:"render",value:function(){var e=this;console.log(this.props);var t=this.createDropDownList(this.state.cat_options),a=this.createDropDownList(v),n=this.createDropDownList(k),l={start:this.state.score||.25,min:0,max:.5,step:.125,onChange:function(t){e.setState({score:t})}},o=this.state.isOpen?"chevron down":"chevron right";return r.a.createElement("div",{ref:this.advanced},r.a.createElement("br",null),r.a.createElement(g.a,{onSubmit:this.handleSubmit,size:"large",key:"large"},r.a.createElement(g.a.Input,{placeholder:"Enter your search",name:"search",type:"text",onChange:this.handleChange,value:this.state.search,focus:!0}),r.a.createElement(E.a,null,r.a.createElement(E.a.Title,{onClick:this.handleAdvanced},r.a.createElement("h4",null,r.a.createElement(f.a,{name:o})," Advanced Search"))),this.state.isOpen?r.a.createElement("div",null,r.a.createElement(g.a.Dropdown,{closeOnChange:!0,placeholder:"Select Categories",name:"categories",label:"Categories",multiple:!0,search:!0,selection:!0,options:t,onChange:this.handleChange,value:this.state.categories,clearable:!0,focus:!0}),r.a.createElement(g.a.Group,{widths:"equal"},r.a.createElement(g.a.Field,null,r.a.createElement("p",null,r.a.createElement("b",null,"Relevancy \u2003vs. \xa0\u2002Funny Factor")),r.a.createElement(b.Slider,{discrete:!0,color:"white",settings:l})),r.a.createElement(g.a.Dropdown,{placeholder:"Select Maturity",name:"maturity",label:"Maturity Rating",selection:!0,clearable:!0,options:n,onChange:this.handleChange,value:this.state.maturity}),r.a.createElement(g.a.Dropdown,{placeholder:"Select Joke Length",name:"sizes",label:"Joke Length",selection:!0,clearable:!0,multiple:!0,options:a,onChange:this.handleChange,value:this.state.sizes,focus:!0,closeOnChange:!0}))):null,this.state.displayMessage?r.a.createElement("h5",{style:{color:"black"}},'Please provide an input for "Keywords", "Categories", "Maturity" or "Joke Length" to search.'):null,r.a.createElement(g.a.Group,{inline:!0,style:{justifyContent:"center",alignItems:"center"}},r.a.createElement(g.a.Button,{secondary:!0,type:"submit",size:"large"},"Find Jokes"),r.a.createElement(g.a.Button,{primary:!0,size:"large",onClick:this.handleLucky},"I'm Feeling Funny!"))))}}]),a}(r.a.Component),C=Object(y.f)(w),O=a(107),S=a(443),_=a(130),L=a.n(_),D=a(441),P=a(131),x=function(e){var t=e.cos_score,a=e.jac_score,n=e.sc_score,l=e.similarity;return r.a.createElement(S.a,{position:"right center",trigger:r.a.createElement(f.a,{className:"info_icon",color:"teal",name:"question circle",size:"large"}),hoverable:!0},r.a.createElement(S.a.Header,null,"Similarity Score Breakdown"),r.a.createElement(S.a.Content,null,r.a.createElement(P.a,{data:{labels:["Keywords (%)","Categories (%)","Funny Factor (%)"],datasets:[{label:"breakdown",backgroundColor:["#FDC144","#FD6585","#3DA3E8"],hoverBackgroundColor:["#FEDB93","#FEBCCA","#3DCEE8"],data:[Number((Number(t)/Number(l)*100).toFixed(1)),Number((Number(a)/Number(l)*100).toFixed(1)),Number((Number(n)/Number(l)*100).toFixed(1))]}]},options:{legend:{display:!0,position:"right",fontSize:4}}})))},F=function(e){Object(c.a)(a,e);var t=Object(u.a)(a);function a(){return Object(i.a)(this,a),t.apply(this,arguments)}return Object(s.a)(a,[{key:"render",value:function(){console.log(this.props);var e=this.props,t=e.jokes,a=e.query;return 0===t.length?r.a.createElement(r.a.Fragment,null):r.a.createElement(r.a.Fragment,null,t.map((function(e,t){return t<=20?r.a.createElement("div",{key:t},r.a.createElement("div",{className:"card"},r.a.createElement("div",{className:"card-body"},e.text.split("\n").map((function(e,t){return r.a.createElement("h5",{key:t},r.a.createElement(L.a,{highlightClassName:"Highlight",searchWords:a,autoEscape:!0,textToHighlight:e}))})),e.categories.map((function(e,t){return r.a.createElement(O.a,{key:t},e)})),r.a.createElement("div",null,r.a.createElement(S.a,{content:e.score,position:"right center",trigger:r.a.createElement("h6",{className:"star_hover"},r.a.createElement(D.a,{className:"rating_stars",name:"half-rating-read",defaultValue:parseFloat(e.score),precision:.1,readOnly:!0}))})),r.a.createElement("h6",{className:"sim_sc_display"},"Similarity Score: ",Number((100*Number(e.similarity)).toFixed(1))+"%"),r.a.createElement(x,{cos_score:e.cos_score,jac_score:e.jac_score,sc_score:e.sc_score,similarity:e.similarity}))),r.a.createElement("br",null)):null})))}}]),a}(r.a.Component),z=a(222),N=a.n(z),A=function(e){Object(c.a)(a,e);var t=Object(u.a)(a);function a(e){var n;return Object(i.a)(this,a),(n=t.call(this,e)).handleClick=n.handleClick.bind(Object(p.a)(n)),n}return Object(s.a)(a,[{key:"handleClick",value:function(e){e.preventDefault(),this.props.history.push({pathname:"/"})}},{key:"render",value:function(){return r.a.createElement("div",{onClick:this.handleClick,style:{cursor:"pointer"}},r.a.createElement("header",{className:"App-header"},r.a.createElement("h1",null,"HahaFactory:"),r.a.createElement("h2",null,"Finding Hilarious Jokes for You"),r.a.createElement("img",{src:N.a,className:"App-logo",alt:"logo",onClick:this.handleClick})))}}]),a}(r.a.Component),q=Object(y.f)(A),G=a(438),J=a(439),R=a(446),M=a(437),T=a(447),B=a(440),W=function(e){Object(c.a)(a,e);var t=Object(u.a)(a);function a(e){var n;return Object(i.a)(this,a),(n=t.call(this,e)).state={isLoaded:!1,jokes:[],typo:!1,typo_query:"",query:[],categories:[],score:"",search:"",sizes:[],maturity:""},n}return Object(s.a)(a,[{key:"componentDidMount",value:function(){this.fetchResults()}},{key:"fetchResults",value:function(){var e=this,t=new URLSearchParams(window.location.search),a=t.getAll("categories"),n=t.get("score"),r=t.get("search"),l=t.getAll("sizes"),o=t.get("maturity");m()({method:"GET",url:"/api/search",params:t}).then((function(t){e.setState({isLoaded:!0,jokes:t.data.jokes,typo:t.data.typo,typo_query:t.data.typo_query,query:t.data.query,categories:a,score:n,search:r,sizes:l,maturity:o})})).catch((function(e){return console.log(e)}))}},{key:"componentDidUpdate",value:function(e){!1===this.state.isLoaded&&this.fetchResults()}},{key:"render",value:function(){return this.state.isLoaded?r.a.createElement("div",null,r.a.createElement("div",null,r.a.createElement(R.a,{style:{margin:"5px"},onClick:function(){return window.open("/about","_blank")}}," About ")),r.a.createElement("div",{style:{alignItems:"center",justify:"center",maxWidth:"50%",left:"25%",position:"absolute"}},r.a.createElement(M.a,null,r.a.createElement(G.a,{className:"justify-content-md-center"},r.a.createElement(J.a,null,r.a.createElement(q,null),r.a.createElement(C,{score:this.state.score,categories:this.state.categories,search:this.state.search,sizes:this.state.sizes,maturity:this.state.maturity}))),r.a.createElement(G.a,null,r.a.createElement(J.a,{className:"jokes-col"},this.state.typo&""===this.state.typo_query?r.a.createElement("div",null,r.a.createElement("h4",null," We could not find any results for ",r.a.createElement("b",null,'"',this.state.search,'"'),".")):null,this.state.typo&""!==this.state.typo_query?r.a.createElement("div",null,r.a.createElement("h4",null," Did you mean... ",r.a.createElement("b",null,'"',this.state.typo_query,'"'),"? "),r.a.createElement("h4",null," We are showing results for ",r.a.createElement("b",null,'"',this.state.typo_query,'"'),".")):null,r.a.createElement(F,{jokes:this.state.jokes,query:this.state.query,search:this.state.search}),r.a.createElement("p",{style:{textAlign:"center",marginTop:"13px"}}," Created by: Cathy Xin, Jason Jung, Rachel Han, Suin Jung, Winice Hui")))))):r.a.createElement(T.a,{active:!0,inverted:!0},r.a.createElement(B.a,{size:"large"},"Loading... "))}}],[{key:"getDerivedStateFromProps",value:function(e,t){var a=new URLSearchParams(e.location.search),n=a.getAll("categories"),r=a.get("score"),l=a.get("search"),o=a.getAll("sizes"),i=a.get("maturity"),s=n.sort().toString()!==t.categories.sort().toString(),c=o.sort().toString()!==t.sizes.sort().toString();return s||r!==t.score||l!==t.search||c||i!==t.maturity?{isLoaded:!1}:null}}]),a}(r.a.Component),H=a(224),I=a.n(H),U=a(225),Y=a.n(U),K=a(226),V=a.n(K),X=function(e){Object(c.a)(a,e);var t=Object(u.a)(a);function a(e){var n;return Object(i.a)(this,a),(n=t.call(this,e)).handleClick=n.handleClick.bind(Object(p.a)(n)),n}return Object(s.a)(a,[{key:"handleClick",value:function(e){e.preventDefault(),this.props.history.push({pathname:"/"})}},{key:"render",value:function(){return r.a.createElement(r.a.Fragment,null,r.a.createElement(q,null),r.a.createElement("div",{style:{alignItems:"center",justify:"center",maxWidth:"55%",left:"22.5%",position:"absolute",margin:"20px"}},r.a.createElement("div",{style:{textAlign:"center"}},r.a.createElement("h2",null," Need a ",r.a.createElement("b",null,"pick-up line"),"?"),r.a.createElement("h2",null,"A ",r.a.createElement("b",null,"funny opener")," for your upcoming speech? "),r.a.createElement("h2",null,"Or can\u2019t remember the ",r.a.createElement("b",null,"punchline")," of a joke you\u2019ve heard before? \u2026 "),r.a.createElement("br",null),r.a.createElement("h3",{style:{color:"#303030"}}," Then ",r.a.createElement("b",null," HahaFactory")," is the perfect place for you to find a laugh! ")),r.a.createElement("h4",{style:{color:"#303030"}},r.a.createElement("br",null),"With jokes scraped from numerous sources covering different categories, types, maturity and length, our joke recommendation engine helps ",r.a.createElement("b",null,"you")," find appropriate jokes for ",r.a.createElement("b",null,"any and every occassion."),r.a.createElement("hr",null),"Our ",r.a.createElement("b",null,"simple search")," allows you to input any keywords to your search, and relevant results will be displayed.",r.a.createElement("br",null),r.a.createElement("br",null),"If you would like to refine your search further, the ",r.a.createElement("b",null," advanced search")," allows you to manually add joke categories, adjust the relevancy vs. funny factor, and filter jokes based on maturity and length.",r.a.createElement("br",null),r.a.createElement("br",null),"Below is an example of a sample input.",r.a.createElement("br",null),r.a.createElement("br",null),r.a.createElement("img",{src:I.a,style:{width:"100%",height:"100%"}}),r.a.createElement("br",null),r.a.createElement("br",null),"Relevant results are outputted with each joke displaying its joke score, a similarity score, and any relevant categories it falls under.",r.a.createElement("br",null),r.a.createElement("br",null),r.a.createElement("img",{src:Y.a,style:{width:"75%",height:"75%",left:"13%",position:"relative"}}),r.a.createElement("br",null),r.a.createElement("br",null),"The ",r.a.createElement("b",null," Joke Score")," is an indication of how funny the joke is. These scores were accumulated and standardized across our different data sources, and learned through KNN clustering.",r.a.createElement("br",null),r.a.createElement("br",null),"The ",r.a.createElement("b",null," Similarity Score")," is an indication of how relevant the joke is to the inputted query. Results are ranked based on similarity score.",r.a.createElement("br",null),r.a.createElement("br",null),r.a.createElement("img",{src:V.a,style:{width:"75%",height:"75%",left:"13%",position:"relative"}}),r.a.createElement("br",null),r.a.createElement("br",null),"To gain a better understanding of this score, you may hover over the similarity score number to see a ",r.a.createElement("b",null,"visual breakdown."),"The percent displayed corresponds to the weight that the corresponding input contributed to the total similarity score.",r.a.createElement("hr",null),"Our algorithm currently uses a ",r.a.createElement("b",null,"combination of similarity measurements "),"(fast jaccard, and fast cosine) and and a ",r.a.createElement("b",null," unique weighting system ")," to help you find results that are not only relevant, but also funny. Some additional features in our engine include ",r.a.createElement("b",null,"typo recognition "),"and an ",r.a.createElement("b",null,'"I\'m Feeling Funny" '),"random joke generator.",r.a.createElement("br",null),r.a.createElement("br",null),"We hope that you enjoy this insight into your results and find our recommendation engine fun! Have fun generating some more laughs!",r.a.createElement("br",null),r.a.createElement("br",null)),r.a.createElement("h4",{style:{textAlign:"center",color:"white"}},r.a.createElement("a",{href:"http://hahafactory-og.herokuapp.com/",target:"_blank",style:{margin:"20px"}},"First Prototype"),r.a.createElement("a",{href:"http://hahafactory-v2.herokuapp.com/",target:"_blank",style:{margin:"20px"}},"Second Prototype"),r.a.createElement("a",{href:"http://hahafactory.herokuapp.com/",target:"_blank",style:{margin:"20px"}},"Third Prototype")),r.a.createElement(R.a,{color:"white",size:"large",style:{left:"38%",position:"absolute",margin:"20px"},onClick:this.handleClick},"Back to Search")))}}]),a}(r.a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));var $=a(227);o.a.render(r.a.createElement($.a,null,r.a.createElement(y.c,null,r.a.createElement(y.a,{path:"/about",component:X}),r.a.createElement(y.a,{path:"/",component:W}))),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}},[[243,1,2]]]);
//# sourceMappingURL=main.80f66d60.chunk.js.map