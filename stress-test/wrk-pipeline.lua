-- example script demonstrating HTTP pipelining

init = function(args)
    local r = {}
    r[1] = wrk.format(nil, "/icpIIBtest?1")
    r[2] = wrk.format(nil, "/icpIIBtest?2")
    r[3] = wrk.format(nil, "/icpIIBtest?3")
    r[4] = wrk.format(nil, "/icpIIBtest?4")
    r[5] = wrk.format(nil, "/icpIIBtest?5")
    r[6] = wrk.format(nil, "/icpIIBtest?6")
    r[7] = wrk.format(nil, "/icpIIBtest?7")

    req = table.concat(r)
end

request = function()
    return req
end
