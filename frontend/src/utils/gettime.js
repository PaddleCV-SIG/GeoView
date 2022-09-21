//https://blog.csdn.net/qq_32058147/article/details/123840125计时器
function getCurrentTime() {
    //获取当前时间并打印
    this.currentyear = new Date().getFullYear();
    this.currentmonth = new Date().getMonth() + 1;
    this.currentday = new Date().getDate();
    this.currenthour = new Date().getHours();
    this.currentminute =
        new Date().getMinutes() < 10
            ? "0" + new Date().getMinutes()
            : new Date().getMinutes();
    this.currentsecond =
        new Date().getSeconds() < 10
            ? "0" + new Date().getSeconds()
            : new Date().getSeconds();
    this.getDate = setTimeout(this.getCurrentTime, 1000);
}

export { getCurrentTime }