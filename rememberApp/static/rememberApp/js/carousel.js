let offset1 = 0;
const slides = document.querySelector('.slides');
document.querySelector('.next').addEventListener('click', function () {
   offset1 = offset1 + 405;
   if (offset1 > 1215) {
      offset1 = 0;
   }
   slides.style.left = -offset1 + 'px';
});
document.querySelector('.prev').addEventListener('click', function () {
   offset1 = offset1 - 405;
   if (offset1 < 0) {
      offset1 = 1215;
   }
   slides.style.left = -offset1 + 'px';
});
