Intended Solve:

- From the sunshinectf2025 profile, find the SunshineCTF group.
- Go into the store on the Sunshine CTF group and find the shirt. According to it's description, the shirt is only for sunshinectf2025
- Create a workspace in Roblox Studio
- Execute `game.Players:CreateHumanoidModelFromUserId(9425269883).Parent = workspace`
- We obtain `9425269883` from the `userId` of the `sunshinectf2025` account.
- Copy the value of the `ShirtTemplate` property owned by the Player model in Workspace (http://www.roblox.com/asset/?id=99859692989451)
- Create a part and place a decal inside of it
- Modify the `Texture` property of the decal to the previously copied value of `ShirtTemplate`
- Modify the shape/size of the part as needed until the flag is visible.
