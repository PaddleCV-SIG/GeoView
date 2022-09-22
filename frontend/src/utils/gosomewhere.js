
function goDetectChanges() {
    this.drawer = false
    if (this.$route.path === "/detectchanges") {
        this.$message.success('您已经在该界面了哦')
    } else this.$router.push("detectchanges");
}
function goDetectTargets() {
    this.drawer = false;
    if (this.$route.path === "/detecttargets") {
        this.$message.success('您已经在该界面了哦')
    } else this.$router.push("detecttargets");
}
function goClassify() {
    this.drawer = false;
    if (this.$route.path === "/classify") {
        this.$message.success('您已经在该界面了哦')
    } else this.$router.push("classify");
}
function goOnlineMap(){
    this.drawer = false
    if (this.$route.path === "/onlinemap") {
        this.$message.success('您已经在该界面了哦')
    } else this.$router.push("onlinemap");
}
function goHistory() {
    if (this.$route.path === "/history") { this.$message.success('您已经在该界面了哦') }
    else
        this.$router.push({
            name: "history",
  
        });
}
export { goDetectChanges, goDetectTargets, goClassify,goOnlineMap, goHistory }
