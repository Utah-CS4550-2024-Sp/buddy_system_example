import { render, screen, within } from "@testing-library/react";
import { userEvent } from "@testing-library/user-event";
import { currentUser } from "./mocks/fixtures";
import App from "../src/App";

describe("home page", () => {
  const user = userEvent.setup();

  it("shows as not logged in", () => {
    render(<App />);
    screen.getByText("logged in: false");
  });

  describe("top navigation", () => {
    it("has a home link", () => {
      render(<App />);
      const header = screen.getByRole("banner");
      within(header).getByText("home");
    });

    it("has a login link", () => {
      render(<App />);
      const header = screen.getByRole("banner");
      within(header).getByText("login");
    });

    describe("clicking the login link", () => {
      it("shows the login form", async () => {
        render(<App />);
        const header = screen.getByRole("banner");
        const login = within(header).getByText("login");
        await user.click(login);

        screen.getByLabelText("username");
        screen.getByLabelText("password");
      });

      it("has a disabled login button", async () => {
        render(<App />);
        const header = screen.getByRole("banner");
        const loginNavLink = within(header).getByText("login");
        await user.click(loginNavLink);

        const main = screen.getByRole("main");
        const loginButton = within(main).getByText("login");
        expect(loginButton).toBeDisabled();
      });

      it("has an enabled login button after entering username and password", async () => {
        render(<App />);
        const header = screen.getByRole("banner");
        const loginNavLink = within(header).getByText("login");
        await user.click(loginNavLink);

        const main = screen.getByRole("main");
        const loginButton = within(main).getByText("login");
        expect(loginButton).toBeDisabled();
        const usernameInput = within(main).getByLabelText("username");
        const passwordInput = within(main).getByLabelText("password");
        await user.type(usernameInput, "juniper");
        expect(loginButton).toBeDisabled();
        await user.type(passwordInput, "password123");
        expect(loginButton).not.toBeDisabled();
      });

      describe("logging in", () => {
        it("shows the full top navigation", async () => {
          render(<App />);
          const header = screen.getByRole("banner");
          const loginNavLink = within(header).getByText("login");
          await user.click(loginNavLink);

          const main = screen.getByRole("main");
          const loginButton = within(main).getByText("login");
          const usernameInput = within(main).getByLabelText("username");
          const passwordInput = within(main).getByLabelText("password");
          await user.type(usernameInput, "juniper");
          await user.type(passwordInput, "password123");
          await user.click(loginButton);

          within(header).getByText("animals");
          within(header).getByText("counter");
          within(header).findByText(currentUser.username);
        });
      });
    });
  });
});

