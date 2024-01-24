import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarTrigger,
} from "@/components/ui/menubar";
import { ScrollArea } from "@/components/ui/scroll-area";

import { User } from "@/data/interfaces";
import { logout } from "@/utils/api/user";
import { Input } from "./ui/input";
import { Button } from "./ui/button";

interface Props {
  user: User;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

const items: string[] = [];

for (let i = 0; i < 5; i++) {
  items.push("message" + i);
}

export function MainView({ user, setUser }: Props) {
  function apiLogOut(): void {
    logout();
    setUser(null);
  }

  return (
    <div className="flex flex-col h-screen">
      <Menubar>
        <MenubarMenu>
          <MenubarTrigger>{user.name}</MenubarTrigger>
          <MenubarContent>
            <MenubarItem onClick={apiLogOut}>Log out</MenubarItem>
          </MenubarContent>
        </MenubarMenu>
      </Menubar>

      <div className="flex flex-col flex-grow max-h-screen overflow-hidden">
        <ScrollArea className="flex-grow overflow-y-auto">
          {items.map((s, index) => (
            <div key={index}>{s}</div>
          ))}
        </ScrollArea>

        <div className="flex items-center space-x-2">
          <Input type="text" placeholder="Send message to group" />
          <Button type="submit">Send</Button>
        </div>
      </div>
    </div>
  );
}
