-- Convert runs of Unicode superscript characters that fonts often lack (⁻, ⁰, ⁴–⁹) into
-- real superscripts, so "10⁻⁶" renders in every font in both Word and PDF output.
local map = {["⁰"]="0", ["¹"]="1", ["²"]="2", ["³"]="3", ["⁴"]="4", ["⁵"]="5",
             ["⁶"]="6", ["⁷"]="7", ["⁸"]="8", ["⁹"]="9", ["⁻"]="−"}
local risky = {["⁰"]=true, ["⁴"]=true, ["⁵"]=true, ["⁶"]=true, ["⁷"]=true, ["⁸"]=true, ["⁹"]=true, ["⁻"]=true}

function Str(el)
  local t = el.text
  local has = false
  for _, cp in utf8.codes(t) do
    if risky[utf8.char(cp)] then has = true; break end
  end
  if not has then return nil end
  local out, buf, sup = {}, {}, {}
  local function flush_buf() if #buf > 0 then table.insert(out, pandoc.Str(table.concat(buf))); buf = {} end end
  local function flush_sup()
    if #sup > 0 then
      local plain, any = {}, false
      for _, ch in ipairs(sup) do plain[#plain + 1] = map[ch]; if risky[ch] then any = true end end
      if any then table.insert(out, pandoc.Superscript({pandoc.Str(table.concat(plain))}))
      else table.insert(out, pandoc.Str(table.concat(sup))) end
      sup = {}
    end
  end
  for _, cp in utf8.codes(t) do
    local ch = utf8.char(cp)
    if map[ch] then flush_buf(); sup[#sup + 1] = ch
    else flush_sup(); buf[#buf + 1] = ch end
  end
  flush_sup(); flush_buf()
  return out
end
