var jumb=document.getElementById('jumbo');
var count=0
function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}
$('#demoButton').fadeOut();
$('#jumbot').on('mouseover',function(){
  $('#demoButton').fadeIn('slow');
})
$('#jumbot').on('mouseout',function(){
  $('#demoButton').fadeOut('slow');
})
