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

for (let i = 0; i < 100; i++) {
  items.push("message" + i);
}

export function MainView({ user, setUser }: Props) {
  function apiLogOut(): void {
    logout();
    setUser(null);
  }
  return (
    <div className="w-4/5 px-[3%] flex flex-col flex-grow h-full">
      <Menubar>
        <MenubarMenu>
          <MenubarTrigger>{user.name}</MenubarTrigger>
          <MenubarContent>
            <MenubarItem onClick={apiLogOut}>Log out</MenubarItem>
          </MenubarContent>
        </MenubarMenu>
      </Menubar>
      <div className="flex flex-grow py-4 gap-x-4 items-start">
        <ScrollArea className="w-3/5 flex flex-col gap-y-4 overflow-y-auto">
          {items.map((s) => {
            return <div>{s}</div>;
          })}
        </ScrollArea>
      </div>
      <div className="flex w-full items-center space-x-2">
        <Input type="text" placeholder="Send message to group" />
        <Button type="submit">Send</Button>
      </div>
    </div>
  );
}
