-- Map ::: {custom-style="Callout|Safety|Answer|Instructor"} divs to tcolorbox
-- environments for LaTeX output (docx keeps the custom paragraph styles).
local boxes = {Callout=true, Safety=true, Answer=true, Instructor=true}
function Div(el)
  local s = el.attributes["custom-style"]
  if FORMAT:match("latex") and s and boxes[s] then
    table.insert(el.content, 1, pandoc.RawBlock("latex", "\\begin{" .. s .. "}"))
    table.insert(el.content, pandoc.RawBlock("latex", "\\end{" .. s .. "}"))
    return el.content
  end
  -- keep what follows together: ::: {.needspace lines="14"} ::: (LaTeX only; Word keeps headings with the next paragraph)
  if el.classes:includes("needspace") then
    local n = el.attributes["lines"] or "12"
    if FORMAT:match("latex") then return pandoc.RawBlock("latex", "\\needspace{" .. n .. "\\baselineskip}") end
    return {}
  end
  -- page breaks: ::: pagebreak :::
  if el.classes:includes("pagebreak") then
    if FORMAT:match("latex") then return pandoc.RawBlock("latex", "\\clearpage") end
    if FORMAT:match("docx") then
      return pandoc.RawBlock("openxml", '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
    end
  end
end
