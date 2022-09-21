import {request} from  "@/api/request.js"

export function historyGetPage(page,limit,type){
    return request({
        method:'GET',
        url:'/api/history/list',
        params:{
            page:page,
            limit:limit,
            type:type
        }
    })
}

export function historyDelete(data){
    return request({
        method:'DELETE',
        url:'api/history/batchRemove',
        data
    })
}