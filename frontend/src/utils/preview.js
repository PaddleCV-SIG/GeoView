
import global from '@/global'
function previewOnePic(pic) {
    this.flag = 1
    this.fbflag = 1
    this.previewPic1 = global.BASE_IMAGE_URL + pic
    this.preVisible = true;
}
function previewTwoPic(pic1, pic2) {
    this.flag = 2
    this.fbflag = 2
    this.previewPic1 = global.BASE_IMAGE_URL + pic1
    this.previewPic2 = global.BASE_IMAGE_URL + pic2
    this.preVisible = true
}
function previewThreePic(pic1, pic2, pic3) {
    this.flag = 3
    this.fbflag = 3
    this.previewPic1 = global.BASE_IMAGE_URL + pic1
    this.previewPic2 = global.BASE_IMAGE_URL + pic2
    this.previewPic3 = global.BASE_IMAGE_URL + pic3
    this.preVisible = true
}

export { previewOnePic, previewTwoPic, previewThreePic }