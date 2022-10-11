
function goDetectChanges() {
    this.isNavigator = false
    if (this.$route.path === "/detectchanges") {
        this.$message.success('您已经在该界面了哦')
    } else this.$router.push("detectchanges");
}
function goDetectTargets() {
    this.isNavigator = false;
    if (this.$route.path === "/detecttargets") {
        this.$message.success('您已经在该界面了哦')
    } else this.$router.push("detecttargets");
}
function goClassify() {
    this.isNavigator = false;
    if (this.$route.path === "/classify") {
        this.$message.success('您已经在该界面了哦')
    } else this.$router.push("classify");
}

function goClassifyScenes() {
    this.isNavigator = false;
    if (this.$route.path === "/classifyscenes") {
        this.$message.success('您已经在该界面了哦')
    } else this.$router.push("classifyscenes");
}

function goRestoreImgs() {
    this.isNavigator = false;
    if (this.$route.path === "/restoreimgs") {
        this.$message.success('您已经在该界面了哦')
    } else this.$router.push("restoreimgs");
}

function goOnlineMap(){
    this.isNavigator = false
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
export { goDetectChanges, goDetectTargets, goClassify,goClassifyScenes,goRestoreImgs,goOnlineMap,goHistory }
