const shareButton = document.querySelector('#circle');
const shareDialog = document.querySelector('.share-dialog');
const closeButton = document.querySelector('.close-button');

shareButton.addEventListener('click', event => {
  if (navigator.share) {
   navigator.share({
      title: 'WebShare API Demo',
      url: 'https://mybluelinux.com/ayoisaiah/pen/YbNazJ'
    }).then(() => {
      console.log('Thanks for sharing!');
    })
    .catch(console.error);
    } else {
        shareDialog.classList.add('is-open');
    }
});

closeButton.addEventListener('click', event => {
  shareDialog.classList.remove('is-open');
});