Interceptor.attach(Module.findExportByName(null, "memcmp"), {
    onEnter: function (args) {
        var buf1 = Memory.readUtf8String(args[0]);
        var buf2 = Memory.readUtf8String(args[1]);
        console.log("[memcmp] " + buf1 + " vs " + buf2);
    }
});
