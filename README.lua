-- Fake Admin Message GUI (Advanced)
local ScreenGui = Instance.new("ScreenGui", game.CoreGui)
ScreenGui.Name = "AdminFake"

local Frame = Instance.new("Frame", ScreenGui)
Frame.Size = UDim2.new(1,0,0,60)
Frame.Position = UDim2.new(0,0,0,0)
Frame.BackgroundColor3 = Color3.fromRGB(20,20,20)

local TextLabel = Instance.new("TextLabel", Frame)
TextLabel.Size = UDim2.new(1,0,1,0)
TextLabel.BackgroundTransparency = 1
TextLabel.TextColor3 = Color3.fromRGB(255, 60, 60)
TextLabel.TextScaled = true
TextLabel.Font = Enum.Font.SourceSansBold

-- Fake countdown
for i = 10,1,-1 do
    TextLabel.Text = "[ADMIN]: Server sẽ reset trong "..i.." giây!"
    wait(1)
end

TextLabel.Text = "[ADMIN]: Đang shutdown server..."

-- Nhấp nháy nhanh hơn khi “cao trào”
for i = 1,10 do
    TextLabel.Visible = not TextLabel.Visible
    wait(0.2)
end

TextLabel.Text = "[SYSTEM]: Mất kết nối!"
