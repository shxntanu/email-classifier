import {
    CardTitle,
    CardDescription,
    CardHeader,
    CardContent,
    Card,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function App() {
    return (
        <div className="flex items-center justify-center min-h-[400px]">
            <Card className="w-full max-w-sm">
                <CardHeader className="space-y-2">
                    <CardTitle className="text-center">EC Feedback</CardTitle>
                    <CardDescription className="text-center">
                        Which department should the email have been routed to?
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <Input placeholder="" type="email" />
                    <Button
                        className="w-full"
                        type="submit"
                        onClick={() => {
                            alert("Thank you for the feedback!");
                        }}
                    >
                        Submit
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
