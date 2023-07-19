$("#raymond").validate({
    rules:{
    //     controller:{
    //       required:false,
    //       remote:{
    //         url:window.location.origin+"/check_controller",
    //         type:"get",
    //         data:{
            
    //         }
            
    //       }
    //   },
      project_number:{
        required:true,
      },
      project_name:{
        required:true,
      },
      standard:{
        required:true,
      },
      system_tag:{
        required:true,
      },
      controller:{
        required:true,
      },
      platform:{
        required:true,
      },
      interface:{
        required:true,
      },
      system_medium:{
        required:true,
      },
      system_type:{
        required:true,
      },
      // control_sec:{
      //   required:true,
      // },
      
   },
});